"""
Use case para crear customers usando auth_service y user_service
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_internal_error, raise_conflict_error
from ..utils.error_handler import handle_auth_service_error
from ....domain.customer.dto.requests.customer_requests import CreateCustomerRequest
from ....domain.customer.dto.responses.customer_responses import CustomerResponse


class CreateCustomerUseCase:
    """Use case para crear customers usando auth_service y user_service"""
    
    def __init__(self):
        self.auth_service_url = config.AUTH_SERVICE_URL
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, request: CreateCustomerRequest, access_token: str = None) -> CustomerResponse:
        """
        Crear customer en Firebase y luego en la base de datos
        
        Args:
            request: DTO con los datos del customer
            access_token: Token de acceso para las llamadas a los servicios
            
        Returns:
            CustomerResponse: Customer creado
        """
        auth_user = None
        user_id = None
        
        try:
            # 1. Crear usuario en Firebase (auth_service)
            auth_user = await self._create_firebase_user(request, access_token)
            user_id = auth_user["user_id"]
            
            # 2. Crear customer en la base de datos (user_service)
            db_customer = await self._create_db_customer(request, user_id, access_token)
            
            return db_customer
            
        except Exception as e:
            # Si se creó el usuario en Firebase pero falló la creación en la BD,
            # eliminar el usuario de Firebase para mantener la integridad
            if auth_user and user_id:
                try:
                    await self._delete_firebase_user(user_id, access_token)
                except Exception as delete_error:
                    # Log el error pero no lo lanzamos para no ocultar el error original
                    print(f"⚠️ Error al eliminar usuario de Firebase durante rollback: {delete_error}")
            
            # Manejar el error original
            handle_auth_service_error(e)
    
    async def _create_firebase_user(self, request: CreateCustomerRequest, access_token: str) -> dict:
        """Crear usuario en Firebase"""
        async with APIClient(self.auth_service_url, access_token) as client:
            # Preparar datos para Firebase
            firebase_data = {
                "email": request.email,
                "password": request.password,
                "display_name": request.company_name,
                "phone_number": None,
                "two_factor_enabled": request.two_factor_enabled,
                "send_email_verification": request.send_email_verification
            }
            
            response = await client.post(f"{config.API_PREFIX}/auth/register", data=firebase_data)
            return response
    
    async def _create_db_customer(self, request: CreateCustomerRequest, firebase_uid: str, access_token: str) -> CustomerResponse:
        """Crear customer en la base de datos"""
        async with APIClient(self.user_service_url, access_token) as client:
            # Preparar datos para la BD
            db_data = {
                "auth_uid": firebase_uid,
                "ruc": request.ruc,
                "company_name": request.company_name,
                "email": request.email,
                "username": request.username,
                "phone": request.phone,
                "cellphone_number": request.cellphone_number,
                "cellphone_country_code": request.cellphone_country_code,
                "address": {
                    "street": request.address.street,
                    "city_id": request.address.city_id,
                    "state_id": request.address.state_id,
                    "country_id": request.address.country_id,
                    "postal_code": request.address.postal_code,
                    "additional_info": request.address.additional_info
                },
                "is_active": request.is_active
            }
            
            response = await client.post(f"{config.API_PREFIX}/customers/", data=db_data)
            return CustomerResponse(**response)
    
    async def _delete_firebase_user(self, auth_uid: str, access_token: str) -> None:
        """
        Eliminar usuario de Firebase
        
        Args:
            auth_uid: ID del usuario en Firebase
            access_token: Token de acceso para las llamadas a los servicios
        """
        try:
            async with APIClient(self.auth_service_url, access_token) as client:
                await client.delete(f"{config.API_PREFIX}/auth/users/{auth_uid}")
                print(f"✅ Usuario de Firebase '{auth_uid}' eliminado correctamente")
        except Exception as e:
            print(f"❌ Error al eliminar usuario de Firebase '{auth_uid}': {str(e)}")
            raise