"""
Caso de uso para asignar permisos a usuarios
"""
from ...domain.interfaces import IAuthProvider, IUserClaimsManager
from ...domain.exceptions import AuthError, AuthErrorCode


class AssignPermissionUseCase:
    """Caso de uso para asignar permisos"""
    
    def __init__(self, auth_provider: IAuthProvider, claims_manager: IUserClaimsManager):
        self._auth_provider = auth_provider
        self._claims_manager = claims_manager
    
    def execute(self, user_id: str, permission: str) -> None:
        """Ejecutar caso de uso de asignación de permiso"""
        try:
            # Verificar que el usuario existe
            user = self._auth_provider.get_user_by_id(user_id)
            if not user:
                raise AuthError("Usuario no encontrado", AuthErrorCode.USER_NOT_FOUND.value)
            
            # Asignar permiso
            self._claims_manager.add_user_permission(user_id, permission)
            
        except AuthError:
            raise
        except Exception as e:
            raise AuthError(f"Error al asignar permiso: {str(e)}", AuthErrorCode.USER_NOT_FOUND.value) 