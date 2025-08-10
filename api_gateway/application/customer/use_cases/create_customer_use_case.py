"""
Use case para crear customers usando auth_service y user_service
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_internal_error, raise_conflict_error
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
        try:
            # 1. Crear usuario en Firebase (auth_service)
            auth_user = await self._create_firebase_user(request, access_token)
            
            # 2. Crear customer en la base de datos (user_service)
            user_id = auth_user["user_id"]
            db_customer = await self._create_db_customer(request, user_id, access_token)
            
            return db_customer
            
        except Exception as e:
            # Si falla la creación en la BD, deberíamos eliminar el usuario de Firebase
            # Por simplicidad, solo lanzamos el error
            raise_internal_error(
                message=f"Error creando customer: {str(e)}",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
            )
    
    async def _create_firebase_user(self, request: CreateCustomerRequest, access_token: str) -> dict:
        """Crear usuario en Firebase"""
        try:
            async with APIClient(self.auth_service_url, access_token) as client:
                # Preparar datos para Firebase
                firebase_data = {
                    "email": request.email,
                    "password": request.password,
                    "display_name": request.company_name,
                    "phone_number": request.phone,
                    "two_factor_enabled": request.two_factor_enabled,
                    "send_email_verification": request.send_email_verification
                }
                
                response = await client.post(f"{config.API_PREFIX}/auth/register", data=firebase_data)
                return response
                
        except Exception as e:
            error_message = str(e)
            if "PHONE_NUMBER_EXISTS" in error_message or "phone number already exists" in error_message.lower():
                raise_conflict_error(
                    message="El número de teléfono ya existe en el sistema. Intente con otro número.",
                    error_code=ErrorCode.PHONE_NUMBER_EXISTS.value
                )
            elif "already exists" in error_message.lower() or "already registered" in error_message.lower():
                raise_conflict_error(
                    message="El customer ya existe en Firebase",
                    error_code=ErrorCode.USER_ALREADY_EXISTS.value
                )
            else:
                raise_internal_error(
                    message=f"Error creando customer en Firebase: {error_message}",
                    error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
                )
    
    async def _create_db_customer(self, request: CreateCustomerRequest, firebase_uid: str, access_token: str) -> CustomerResponse:
        """Crear customer en la base de datos"""
        try:
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
                
        except Exception as e:
            raise_internal_error(
                message=f"Error creando customer en la base de datos: {str(e)}",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
            ) 