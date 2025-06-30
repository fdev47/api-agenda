"""
Excepciones del dominio de autenticación
"""
from .auth_exceptions import AuthError, AuthErrorCode

__all__ = [
    'AuthError',
    'AuthErrorCode'
] 