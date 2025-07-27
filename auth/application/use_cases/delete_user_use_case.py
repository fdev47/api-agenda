"""
Use case para eliminar usuario de Firebase Auth
"""
from typing import Protocol
from ...domain.exceptions.auth_exceptions import AuthException, UserNotFoundException


class AuthProvider(Protocol):
    """Protocolo para el proveedor de autenticación"""
    def delete_user(self, user_id: str) -> bool:
        ...


class DeleteUserUseCase:
    """Use case para eliminar usuario de Firebase"""
    
    def __init__(self, auth_provider: AuthProvider):
        self.auth_provider = auth_provider
    
    def execute(self, user_id: str) -> bool:
        """
        Eliminar usuario de Firebase
        
        Args:
            user_id: ID del usuario a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            return self.auth_provider.delete_user(user_id)
        except UserNotFoundException:
            raise
        except AuthException:
            raise
        except Exception as e:
            raise AuthException(f"Error inesperado al eliminar usuario: {str(e)}") 