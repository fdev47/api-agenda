"""
Use case para cambiar contraseña por username de usuario
"""
import logging
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_not_found_error
from ....domain.auth.dto.requests.auth_requests import ChangePasswordByUsernameRequest
from ....domain.auth.dto.responses.auth_responses import ChangePasswordByUsernameResponse

logger = logging.getLogger(__name__)


class ChangePasswordByUserUsernameUseCase:
    """Use case para cambiar contraseña de usuario por username"""
    
    def __init__(self):
        self.auth_service_url = config.AUTH_SERVICE_URL
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, request: ChangePasswordByUsernameRequest, access_token: str = None) -> ChangePasswordByUsernameResponse:
        """
        Cambiar contraseña de usuario por username
        
        Steps:
        1. Obtener usuario por username desde user_service
        2. Extraer auth_uid del usuario
        3. Llamar al auth_service para cambiar contraseña usando auth_uid
        
        Args:
            request: DTO con username y nueva contraseña
            access_token: Token de acceso para las llamadas a los servicios
            
        Returns:
            ChangePasswordByUsernameResponse: Respuesta del cambio de contraseña
        """
        try:
            # 1. Obtener usuario por username desde user_service
            logger.info(f"🔍 Buscando usuario con username: {request.username}")
            async with APIClient(self.user_service_url, access_token) as client:
                user_response = await client.get(
                    f"{config.API_PREFIX}/users/by-username/{request.username}"
                )
            
            # 2. Extraer auth_uid del usuario
            auth_uid = user_response.get("auth_uid")
            if not auth_uid:
                raise_not_found_error(
                    message=f"Usuario con username '{request.username}' no tiene auth_uid",
                    error_code=ErrorCode.USER_NOT_FOUND.value
                )
            
            logger.info(f"✅ Usuario encontrado con auth_uid: {auth_uid}")
            
            # 3. Llamar al auth_service para cambiar contraseña usando auth_uid
            async with APIClient(self.auth_service_url) as client:
                auth_data = {
                    "user_id": auth_uid,
                    "new_password": request.new_password
                }
                
                response = await client.post(
                    f"{config.API_PREFIX}/auth/change-password-by-user-id",
                    data=auth_data
                )
            
            logger.info(f"✅ Contraseña cambiada exitosamente para usuario: {request.username}")
            
            return ChangePasswordByUsernameResponse(
                success=response.get("success", True),
                message=f"Contraseña actualizada exitosamente para usuario {request.username}",
                username=request.username,
                user_type="user"
            )
            
        except Exception as e:
            logger.error(f"❌ Error cambiando contraseña para usuario {request.username}: {str(e)}")
            raise

