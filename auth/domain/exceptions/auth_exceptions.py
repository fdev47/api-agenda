"""
Excepciones de autenticación del dominio
"""
from enum import Enum
from typing import Optional


class AuthError(Exception):
    """Excepción personalizada para errores de autenticación"""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.error_code = error_code


class AuthErrorCode(Enum):
    """Códigos de error estándar"""
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    WEAK_PASSWORD = "WEAK_PASSWORD"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    USER_DISABLED = "USER_DISABLED"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS" 