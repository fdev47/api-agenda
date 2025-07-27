"""
Use case para crear usuarios usando auth_service y user_service
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_internal_error, raise_conflict_error
from ....domain.dto.requests.user_requests import CreateUserRequest
from ....domain.dto.responses.user import UserResponse


class CreateUserUseCase:
    """Use case para crear usuarios usando auth_service y user_service"""
    
    def __init__(self):
        self.auth_service_url = config.AUTH_SERVICE_URL
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, request: CreateUserRequest, access_token: str = None) -> UserResponse:
        """
        Crear usuario en Firebase y luego en la base de datos
        
        Args:
            request: DTO con los datos del usuario
            access_token: Token de acceso para las llamadas a los servicios
            
        Returns:
            UserResponse: Usuario creado
        """
        try:
            # 1. Crear usuario en Firebase (auth_service)
            #auth_user = await self._create_firebase_user(request, access_token)
            
            # 2. Crear usuario en la base de datos (user_service)
            #user_id = auth_user["user_id"]
            user_id = "emQy1KAxP5XU0g3No6dKs3KB1tz2"
            db_user = await self._create_db_user(request, user_id, access_token)
            
            return db_user
            
        except Exception as e:
            # Si falla la creación en la BD, deberíamos eliminar el usuario de Firebase
            # Por simplicidad, solo lanzamos el error
            raise_internal_error(
                message=f"Error creando usuario: {str(e)}",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
            )
    
    async def _create_firebase_user(self, request: CreateUserRequest, access_token: str) -> dict:
        """Crear usuario en Firebase"""
        try:
            async with APIClient(self.auth_service_url, access_token) as client:
                # Preparar datos para Firebase
                display_name = f"{request.first_name or ''} {request.last_name or ''}".strip()
                phone_number = None
                if request.cellphone_number and request.cellphone_country_code:
                    phone_number = f"{request.cellphone_country_code}{request.cellphone_number}"
                elif request.cellphone_number:
                    phone_number = request.cellphone_number
                elif request.phone:
                    phone_number = request.phone
                
                firebase_data = {
                    "email": request.email,
                    "password": request.password,
                    "display_name": display_name,
                    "phone_number": phone_number,
                    "two_factor_enabled": request.two_factor_enabled,
                    "send_email_verification": request.send_email_verification
                }
                
                response = await client.post(f"{config.API_PREFIX}/auth/register", data=firebase_data)
                return response
                
        except Exception as e:
            if "already exists" in str(e).lower() or "already registered" in str(e).lower():
                raise_conflict_error(
                    message="El usuario ya existe en Firebase",
                    error_code=ErrorCode.USER_ALREADY_EXISTS.value
                )
            else:
                raise_internal_error(
                    message=f"Error creando usuario en Firebase: {str(e)}",
                    error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
                )
    
    async def _create_db_user(self, request: CreateUserRequest, firebase_uid: str, access_token: str) -> UserResponse:
        """Crear usuario en la base de datos"""
        try:
            async with APIClient(self.user_service_url, access_token) as client:
                # Preparar datos para la BD
                db_data = {
                    "auth_uid": firebase_uid,
                    "email": request.email,
                    "username": request.username,  # Agregar username
                    "first_name": request.first_name,
                    "last_name": request.last_name,
                    "phone": request.phone,
                    "cellphone_number": request.cellphone_number,
                    "cellphone_country_code": request.cellphone_country_code,
                    "user_type": request.user_type,
                    "profile_ids": [str(pid) for pid in request.profile_ids] if request.profile_ids else []
                }
                
                response = await client.post(f"{config.API_PREFIX}/users/", data=db_data)
                return UserResponse(**response)
                
        except Exception as e:
            raise_internal_error(
                message=f"Error creando usuario en la base de datos: {str(e)}",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
            ) 