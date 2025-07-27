"""
Use case para actualizar usuario en Firebase Auth
"""
from typing import Protocol, Optional
from ...domain.dto.requests.auth_requests import UpdateUserRequest
from ...domain.dto.responses.auth_responses import UserInfoResponse
from ...domain.entities.authenticated_user import AuthenticatedUser
from ...domain.exceptions.auth_exceptions import AuthException, UserNotFoundException


class AuthProvider(Protocol):
    """Protocolo para el proveedor de autenticación"""
    def update_user(self, user_id: str, user_data: UpdateUserRequest) -> AuthenticatedUser:
        ...


class UpdateUserUseCase:
    """Use case para actualizar usuario en Firebase"""
    
    def __init__(self, auth_provider: AuthProvider):
        self.auth_provider = auth_provider
    
    def execute(self, user_id: str, request: UpdateUserRequest) -> UserInfoResponse:
        """
        Actualizar usuario en Firebase
        
        Args:
            user_id: ID del usuario a actualizar
            request: Datos a actualizar
            
        Returns:
            UserInfoResponse: Usuario actualizado
        """
        try:
            user = self.auth_provider.update_user(user_id, request)
            return UserInfoResponse.model_validate(user)
        except UserNotFoundException:
            raise
        except AuthException:
            raise
        except Exception as e:
            raise AuthException(f"Error inesperado al actualizar usuario: {str(e)}") 