"""
Interfaz IAuthProvider del dominio
"""
from abc import ABC, abstractmethod
from typing import Optional
from ..entities import UserRegistration, AuthenticatedUser, AuthToken, UserCredentials, CustomClaims


class IAuthProvider(ABC):
    """Interface principal para proveedores de autenticación"""
    
    @abstractmethod
    def create_user(self, registration: UserRegistration) -> AuthenticatedUser:
        """Crear un nuevo usuario"""
        pass
    
    @abstractmethod
    def authenticate_user(self, credentials: UserCredentials) -> AuthToken:
        """Autenticar un usuario con credenciales"""
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> AuthenticatedUser:
        """Verificar un token de autenticación"""
        pass
    
    @abstractmethod
    def refresh_token(self, refresh_token: str) -> AuthToken:
        """Refrescar un token de acceso"""
        pass
    
    @abstractmethod
    def revoke_token(self, token: str) -> None:
        """Revocar un token"""
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[AuthenticatedUser]:
        """Obtener usuario por ID"""
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[AuthenticatedUser]:
        """Obtener usuario por email"""
        pass
    
    @abstractmethod
    def update_user_claims(self, user_id: str, claims: CustomClaims) -> None:
        """Actualizar claims de un usuario"""
        pass
    
    @abstractmethod
    def disable_user(self, user_id: str) -> None:
        """Deshabilitar un usuario"""
        pass
    
    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        """Eliminar un usuario"""
        pass 