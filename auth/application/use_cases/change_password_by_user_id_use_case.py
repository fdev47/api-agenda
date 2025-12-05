"""
Caso de uso para cambiar contraseña de usuario por user_id
"""
import logging
from ...domain.interfaces.auth_provider import IAuthProvider
from ...domain.dto.requests import ChangePasswordByUserIdRequest
from ...domain.exceptions.auth_exceptions import UserNotFoundException

logger = logging.getLogger(__name__)


class ChangePasswordByUserIdUseCase:
    """Use case para cambiar contraseña usando user_id (auth_uid)"""
    
    def __init__(self, auth_provider: IAuthProvider):
        self.auth_provider = auth_provider
    
    def execute(self, request: ChangePasswordByUserIdRequest) -> dict:
        """
        Cambiar contraseña de un usuario usando su user_id (auth_uid)
        
        Args:
            request: Request con user_id y nueva contraseña
            
        Returns:
            dict con mensaje de éxito
            
        Raises:
            UserNotFoundException: Si el usuario no existe
        """
        try:
            logger.info(f"🔄 Cambiando contraseña para user_id: {request.user_id}")
            
            # Usar el método change_password del auth_provider
            success = self.auth_provider.change_password(request.user_id, request.new_password)
            
            if success:
                logger.info(f"✅ Contraseña cambiada exitosamente para user_id: {request.user_id}")
                return {
                    "success": True,
                    "message": f"Contraseña actualizada exitosamente para user_id {request.user_id}",
                    "user_id": request.user_id
                }
            else:
                logger.error(f"❌ Error cambiando contraseña para user_id: {request.user_id}")
                return {
                    "success": False,
                    "message": "Error al actualizar contraseña",
                    "user_id": request.user_id
                }
                
        except UserNotFoundException:
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado cambiando contraseña: {str(e)}")
            raise

