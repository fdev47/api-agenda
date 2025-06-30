"""
Interfaces del dominio de autenticación
"""
from .auth_provider import IAuthProvider
from .token_validator import ITokenValidator
from .user_claims_manager import IUserClaimsManager

__all__ = [
    'IAuthProvider',
    'ITokenValidator',
    'IUserClaimsManager'
] 