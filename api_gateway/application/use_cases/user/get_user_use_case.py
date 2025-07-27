"""
Use case para obtener usuario desde API Gateway
"""
from typing import Optional, Dict, Any
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_not_found_error, raise_internal_error
from ....domain.dto.responses.user import UserResponse


class GetUserUseCase:
    """Use case para obtener usuario desde User Service"""
    
    def __init__(self):
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, auth_uid: str, access_token: str) -> UserResponse:
        """Ejecutar el use case"""
        try:
            # Crear cliente para User Service con token
            async with APIClient(self.user_service_url, access_token) as client:
                # Obtener usuario del User Service
                response = await client.get(f"{config.API_PREFIX}/users/me")
                
                # Convertir a DTO
                return UserResponse(**response)
                
        except Exception as e:
            # Si el usuario no existe, lanzar error específico
            if "404" in str(e) or "Usuario no encontrado" in str(e):
                raise_not_found_error(
                    message="Usuario no encontrado en el sistema",
                    error_code=ErrorCode.USER_NOT_FOUND.value
                )
            else:
                raise_internal_error(
                    message=f"Error obteniendo usuario: {str(e)}",
                    error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
                ) 