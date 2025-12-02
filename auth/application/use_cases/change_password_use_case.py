"""
Caso de uso para cambiar contraseña de usuario
"""
import logging
from typing import Optional
from ...domain.interfaces.auth_provider import IAuthProvider
from ...domain.dto.requests import ChangePasswordRequest
from ...domain.exceptions.auth_exceptions import UserNotFoundException

logger = logging.getLogger(__name__)


class ChangePasswordUseCase:
    """Caso de uso para cambiar contraseña de un usuario"""
    
    def __init__(self, auth_provider: IAuthProvider):
        self.auth_provider = auth_provider
    
    def execute(self, request: ChangePasswordRequest) -> dict:
        """
        Cambiar contraseña de un usuario basado en su email
        
        Args:
            request: Request con email y nueva contraseña
            
        Returns:
            dict con mensaje de éxito
            
        Raises:
            UserNotFoundException: Si el usuario no existe
        """
        try:
            logger.info(f"🔄 Cambiando contraseña para usuario: {request.email}")
            
            # Obtener usuario por email
            user = self.auth_provider.get_user_by_email(request.email)
            
            if not user:
                logger.warning(f"⚠️ Usuario no encontrado: {request.email}")
                raise UserNotFoundException(request.email)
            
            # Usar el método change_password del auth_provider
            success = self.auth_provider.change_password(user.user_id, request.new_password)
            
            if success:
                logger.info(f"✅ Contraseña cambiada exitosamente para usuario: {request.email}")
                return {
                    "success": True,
                    "message": f"Contraseña actualizada exitosamente para {request.email}"
                }
            else:
                logger.error(f"❌ Error cambiando contraseña para usuario: {request.email}")
                return {
                    "success": False,
                    "message": "Error al actualizar contraseña"
                }
                
        except UserNotFoundException:
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado cambiando contraseña: {str(e)}")
            raise


