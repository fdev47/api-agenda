"""Domain interfaces following Dependency Inversion Principle"""

from abc import ABC, abstractmethod
from typing import Optional, List
from .models import UserRegistration, AuthenticatedUser, AuthToken, UserCredentials, CustomClaims


class IAuthProvider(ABC):
    """Interface principal para proveedores de autenticación"""
    
    @abstractmethod
    def create_user(self, registration: UserRegistration) -> AuthenticatedUser:
        pass
    
    @abstractmethod
    def authenticate_user(self, credentials: UserCredentials) -> AuthToken:
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> AuthenticatedUser:
        pass
    
    @abstractmethod
    def refresh_token(self, refresh_token: str) -> AuthToken:
        pass
    
    @abstractmethod
    def revoke_token(self, token: str) -> None:
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[AuthenticatedUser]:
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[AuthenticatedUser]:
        pass
    
    @abstractmethod
    def update_user_claims(self, user_id: str, claims: CustomClaims) -> None:
        pass
    
    @abstractmethod
    def disable_user(self, user_id: str) -> None:
        pass
    
    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        pass


class ITokenValidator(ABC):
    """Interface para validación de tokens"""
    
    @abstractmethod
    def validate_token_format(self, token: str) -> bool:
        pass
    
    @abstractmethod
    def extract_user_id(self, token: str) -> str:
        pass


class IUserClaimsManager(ABC):
    """Interface para manejo de claims de usuario"""
    
    @abstractmethod
    def set_user_role(self, user_id: str, role: str) -> None:
        pass
    
    @abstractmethod
    def add_user_permission(self, user_id: str, permission: str) -> None:
        pass
    
    @abstractmethod
    def get_user_roles(self, user_id: str) -> List[str]:
        pass 