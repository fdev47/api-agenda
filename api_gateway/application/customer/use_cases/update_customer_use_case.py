"""
Use case para actualizar customers usando auth_service y user_service
"""
from uuid import UUID
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ..utils.error_handler import handle_auth_service_error
from ....domain.customer.dto.requests.customer_requests import UpdateCustomerRequest
from ....domain.customer.dto.responses.customer_responses import CustomerUpdatedResponse


class UpdateCustomerUseCase:
    """Use case para actualizar customers usando auth_service y user_service"""
    
    def __init__(self):
        self.auth_service_url = config.AUTH_SERVICE_URL
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, customer_id: UUID, request: UpdateCustomerRequest, access_token: str = None) -> CustomerUpdatedResponse:
        """
        Actualizar customer en Firebase (si es necesario) y en la base de datos
        
        Args:
            customer_id: ID del customer a actualizar
            request: DTO con los datos a actualizar
            access_token: Token de acceso para las llamadas a los servicios
            
        Returns:
            CustomerUpdatedResponse: Customer actualizado
        """
        try:
            # 1. Obtener información del customer para obtener el auth_uid
            customer_info = await self._get_customer_info(customer_id, access_token)
            auth_uid = customer_info["auth_uid"]
            
            # 2. Determinar si necesitamos actualizar Firebase
            needs_firebase_update = self._needs_firebase_update(request)
            
            if needs_firebase_update:
                await self._update_firebase_user(auth_uid, request, access_token)
            
            # 3. Actualizar customer en la base de datos
            updated_customer = await self._update_db_customer(customer_id, request, access_token)
            
            return updated_customer
            
        except Exception as error:
            handle_auth_service_error(error)
    
    async def _get_customer_info(self, customer_id: UUID, access_token: str) -> dict:
        """Obtener información del customer para obtener el auth_uid"""
        async with APIClient(self.user_service_url, access_token) as client:
                response = await client.get(f"{config.API_PREFIX}/customers/{customer_id}")
                
                # Verificar si la respuesta tiene el formato esperado
                if isinstance(response, dict) and 'customer' in response:
                    # Si la respuesta tiene formato {'customer': {...}}
                    return response['customer']
                else:
                    # Si la respuesta es directa
                    return response
    
    def _needs_firebase_update(self, request: UpdateCustomerRequest) -> bool:
        """Determinar si se necesita actualizar Firebase"""
        # Solo actualizar Firebase si se cambia email o phone
        return request.email is not None or request.phone is not None or request.cellphone_number is not None
    
    async def _update_firebase_user(self, auth_uid: str, request: UpdateCustomerRequest, access_token: str):
        """Actualizar usuario en Firebase"""
        async with APIClient(self.auth_service_url, access_token) as client:
                # Preparar datos para Firebase
                firebase_data = {}
                
                if request.email is not None:
                    firebase_data["email"] = request.email
                
                if request.phone is not None or request.cellphone_number is not None:
                    # Determinar el número de teléfono
                    if request.cellphone_number and request.cellphone_country_code:
                        firebase_data["phone_number"] = f"{request.cellphone_country_code}{request.cellphone_number}"
                    elif request.cellphone_number:
                        firebase_data["phone_number"] = request.cellphone_number
                    elif request.phone:
                        firebase_data["phone_number"] = request.phone
                
                # Solo actualizar si hay datos para Firebase
                if firebase_data:
                    await client.put(f"{config.API_PREFIX}/auth/users/{auth_uid}", data=firebase_data)
    
    async def _update_db_customer(self, customer_id: UUID, request: UpdateCustomerRequest, access_token: str) -> CustomerUpdatedResponse:
        """Actualizar customer en la base de datos"""
        async with APIClient(self.user_service_url, access_token) as client:
            # Preparar datos para la BD (excluir campos que no se pueden actualizar)
            db_data = {}
            
            if request.email is not None:
                db_data["email"] = request.email
            if request.ruc is not None:
                db_data["ruc"] = request.ruc
            if request.company_name is not None:
                db_data["company_name"] = request.company_name
            if request.phone is not None:
                db_data["phone"] = request.phone
            if request.cellphone_number is not None:
                db_data["cellphone_number"] = request.cellphone_number
            if request.cellphone_country_code is not None:
                db_data["cellphone_country_code"] = request.cellphone_country_code
            if request.address is not None:
                db_data["address"] = {
                    "street": request.address.street,
                    "city_id": request.address.city_id,
                    "state_id": request.address.state_id,
                    "country_id": request.address.country_id,
                    "postal_code": request.address.postal_code,
                    "additional_info": request.address.additional_info
                }
            if request.is_active is not None:
                db_data["is_active"] = request.is_active
            
            response = await client.put(f"{config.API_PREFIX}/customers/{customer_id}", data=db_data)
            
            # Verificar si la respuesta tiene el formato esperado
            if isinstance(response, dict) and 'customer' in response:
                # Si la respuesta tiene formato {'customer': {...}}
                customer_data = response['customer']
                return CustomerUpdatedResponse(**customer_data, message="Customer actualizado exitosamente")
            else:
                # Si la respuesta es directa
                return CustomerUpdatedResponse(**response, message="Customer actualizado exitosamente")
