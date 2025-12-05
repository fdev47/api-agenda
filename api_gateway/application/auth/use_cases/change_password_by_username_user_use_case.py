"""
Use case para cambiar contraseña de usuario por username
"""
from commons.api_client import APIClient
from commons.config import config
from ....domain.auth.dto.requests.auth_requests import ChangePasswordByUsernameUserRequest
from ....domain.auth.dto.responses.auth_responses import ChangePasswordByUsernameResponse
from ...user.use_cases.get_user_by_username_use_case import GetUserByUsernameUseCase


class ChangePasswordByUsernameUserUseCase:
    """Use case para cambiar contraseña de usuario por username"""
    
    def __init__(self):
        self.auth_service_url = config.AUTH_SERVICE_URL
        self.get_user_by_username_use_case = GetUserByUsernameUseCase()
    
    async def execute(
        self, 
        request: ChangePasswordByUsernameUserRequest,
        access_token: str = None
    ) -> ChangePasswordByUsernameResponse:
        """
        Cambiar contraseña de usuario por username
        
        Args:
            request: DTO con username y nueva contraseña
            access_token: Token de acceso para llamar a los servicios
            
        Returns:
            ChangePasswordByUsernameResponse: Respuesta del cambio de contraseña
        """
        # 1. Obtener usuario por username para obtener el auth_uid
        user = await self.get_user_by_username_use_case.execute(
            username=request.username,
            access_token=access_token
        )
        
        # 2. Cambiar contraseña usando el auth_uid
        async with APIClient(self.auth_service_url) as client:
            auth_data = {
                "user_id": user.auth_uid,
                "new_password": request.new_password
            }
            
            response = await client.post(
                f"{config.API_PREFIX}/auth/change-password-by-user-id",
                data=auth_data
            )
            
            # 3. Retornar respuesta con username y tipo de usuario
            return ChangePasswordByUsernameResponse(
                success=response.get("success", False),
                message=response.get("message", ""),
                username=request.username,
                user_type="user"
            )

