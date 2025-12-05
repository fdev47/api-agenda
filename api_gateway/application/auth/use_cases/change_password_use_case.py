"""
Use case para cambiar contraseña usando auth_service
"""
from commons.api_client import APIClient
from commons.config import config
from ....domain.auth.dto.requests.auth_requests import ChangePasswordRequest
from ....domain.auth.dto.responses.auth_responses import ChangePasswordResponse


class ChangePasswordUseCase:
    """Use case para cambiar contraseña de usuario en Firebase"""
    
    def __init__(self):
        self.auth_service_url = config.AUTH_SERVICE_URL
    
    async def execute(self, request: ChangePasswordRequest) -> ChangePasswordResponse:
        """
        Cambiar contraseña de usuario en Firebase
        
        Args:
            request: DTO con email y nueva contraseña
            
        Returns:
            ChangePasswordResponse: Respuesta del cambio de contraseña
        """
        async with APIClient(self.auth_service_url) as client:
            # Preparar datos para el auth service
            auth_data = {
                "email": request.email,
                "new_password": request.new_password
            }
            
            # Llamar al endpoint de cambio de contraseña del auth service
            response = await client.post(
                f"{config.API_PREFIX}/auth/change-password", 
                data=auth_data
            )
            
            # Agregar el email a la respuesta
            response["email"] = request.email
            
            return ChangePasswordResponse(**response)

