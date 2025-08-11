"""
Use case para obtener usuario por username desde API Gateway
"""
from typing import Optional, Dict, Any
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_not_found_error, raise_internal_error
from ....domain.user.dto.responses.user_responses import UserResponse
from ..utils.error_handler import handle_auth_service_error

class GetUserByUsernameUseCase:
    """Use case para obtener usuario por username desde User Service"""
    
    def __init__(self):
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, username: str, access_token: str) -> UserResponse:
        """Ejecutar el use case"""
        try:
            # Crear cliente para User Service con token
            async with APIClient(self.user_service_url, access_token) as client:
                # Obtener usuario del User Service por username
                response = await client.get(f"{config.API_PREFIX}/users/by-username/{username}")
                
                # Convertir a DTO
                return UserResponse(**response)
                
        except Exception as e:
            handle_auth_service_error(e)
