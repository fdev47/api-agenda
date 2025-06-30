"""
Caso de uso para obtener roles de usuarios
"""
from typing import List
from ...domain.interfaces import IAuthProvider, IUserClaimsManager
from ...domain.exceptions import AuthError, AuthErrorCode


class GetUserRolesUseCase:
    """Caso de uso para obtener roles de usuarios"""
    
    def __init__(self, auth_provider: IAuthProvider, claims_manager: IUserClaimsManager):
        self._auth_provider = auth_provider
        self._claims_manager = claims_manager
    
    def execute(self, user_id: str) -> List[str]:
        """Ejecutar caso de uso de obtención de roles"""
        try:
            # Verificar que el usuario existe
            user = self._auth_provider.get_user_by_id(user_id)
            if not user:
                raise AuthError("Usuario no encontrado", AuthErrorCode.USER_NOT_FOUND.value)
            
            # Obtener roles
            return self._claims_manager.get_user_roles(user_id)
            
        except AuthError:
            raise
        except Exception as e:
            raise AuthError(f"Error al obtener roles: {str(e)}", AuthErrorCode.USER_NOT_FOUND.value) 