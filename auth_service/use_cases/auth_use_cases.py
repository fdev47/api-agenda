"""Authentication and authorization use cases"""

from typing import List
from auth_service.domain.interfaces import IAuthProvider, ITokenValidator, IUserClaimsManager
from auth_service.domain.models import (
    UserRegistration, AuthenticatedUser, AuthError, AuthErrorCode
)


class CreateUserUseCase:
    """Caso de uso para crear usuarios"""
    
    def __init__(self, auth_provider: IAuthProvider, claims_manager: IUserClaimsManager):
        self._auth_provider = auth_provider
        self._claims_manager = claims_manager
    
    def execute(self, registration: UserRegistration, initial_role: str = "user") -> AuthenticatedUser:
        # Crear usuario
        user = self._auth_provider.create_user(registration)
        
        # Asignar rol inicial
        self._claims_manager.set_user_role(user.user_id, initial_role)
        
        # Retornar usuario actualizado
        return self._auth_provider.get_user_by_id(user.user_id)


class ValidateTokenUseCase:
    """Caso de uso para validar tokens"""
    
    def __init__(self, auth_provider: IAuthProvider, token_validator: ITokenValidator):
        self._auth_provider = auth_provider
        self._token_validator = token_validator
    
    def execute(self, token: str) -> AuthenticatedUser:
        # Validar formato básico
        if not self._token_validator.validate_token_format(token):
            raise AuthError("Formato de token inválido", AuthErrorCode.INVALID_TOKEN.value)
        
        # Verificar token con el proveedor
        return self._auth_provider.verify_token(token)


class ManageUserRolesUseCase:
    """Caso de uso para gestión de roles"""
    
    def __init__(self, auth_provider: IAuthProvider, claims_manager: IUserClaimsManager):
        self._auth_provider = auth_provider
        self._claims_manager = claims_manager
    
    def assign_role(self, user_id: str, role: str) -> None:
        self._claims_manager.set_user_role(user_id, role)
    
    def assign_permission(self, user_id: str, permission: str) -> None:
        self._claims_manager.add_user_permission(user_id, permission)
    
    def get_user_roles(self, user_id: str) -> List[str]:
        return self._claims_manager.get_user_roles(user_id) 