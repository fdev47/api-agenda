"""
Interfaz ITokenValidator del dominio
"""
from abc import ABC, abstractmethod


class ITokenValidator(ABC):
    """Interface para validación de tokens"""
    
    @abstractmethod
    def validate_token_format(self, token: str) -> bool:
        """Validar el formato básico de un token"""
        pass
    
    @abstractmethod
    def extract_user_id(self, token: str) -> str:
        """Extraer el ID de usuario de un token"""
        pass 