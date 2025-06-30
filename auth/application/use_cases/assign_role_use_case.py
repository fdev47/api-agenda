"""
Caso de uso para asignar roles a usuarios
"""
from ...domain.interfaces import IAuthProvider, IUserClaimsManager
from ...domain.exceptions import AuthError, AuthErrorCode


class AssignRoleUseCase:
    """Caso de uso para asignar roles"""
    
    def __init__(self, auth_provider: IAuthProvider, claims_manager: IUserClaimsManager):
        self._auth_provider = auth_provider
        self._claims_manager = claims_manager
    
    def execute(self, user_id: str, role: str) -> None:
        """Ejecutar caso de uso de asignación de rol"""
        try:
            # Verificar que el usuario existe
            user = self._auth_provider.get_user_by_id(user_id)
            if not user:
                raise AuthError("Usuario no encontrado", AuthErrorCode.USER_NOT_FOUND.value)
            
            # Asignar rol
            self._claims_manager.set_user_role(user_id, role)
            
        except AuthError:
            raise
        except Exception as e:
            raise AuthError(f"Error al asignar rol: {str(e)}", AuthErrorCode.USER_NOT_FOUND.value) 