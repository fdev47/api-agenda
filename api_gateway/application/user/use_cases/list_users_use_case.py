"""
Use case para listar usuarios desde API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_internal_error
from ....domain.user.dto.responses.user_responses import UserListResponse
from ..utils.error_handler import handle_auth_service_error

class ListUsersUseCase:
    """Use case para listar usuarios desde User Service"""
    
    def __init__(self):
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, page: int = 1, size: int = 100, branch_code: Optional[str] = None, access_token: str = None) -> UserListResponse:
        """Ejecutar el use case"""
        try:
            # Crear cliente para User Service
            async with APIClient(self.user_service_url, access_token) as client:
                # Preparar parámetros de consulta
                params = {"page": page, "size": size}
                if branch_code:
                    params["branch_code"] = branch_code
                
                # Obtener lista de usuarios del User Service
                response = await client.get(f"{config.API_PREFIX}/users/", params=params)
                
                # Convertir a DTO
                return UserListResponse(**response)
                
        except Exception as e:
            handle_auth_service_error(e)