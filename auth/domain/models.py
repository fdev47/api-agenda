"""Domain models and value objects"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


@dataclass
class AuthToken:
    """Value Object para tokens de autenticación"""
    access_token: str
    refresh_token: Optional[str]
    expires_at: datetime
    token_type: str = "Bearer"


@dataclass
class UserCredentials:
    """Value Object para credenciales de usuario"""
    email: str
    password: str


@dataclass
class UserRegistration:
    """Value Object para registro de usuario"""
    email: str
    password: str
    display_name: Optional[str] = None
    phone_number: Optional[str] = None
    two_factor_enabled: bool = False
    send_email_verification: bool = True


@dataclass
class AuthenticatedUser:
    """Entity para usuario autenticado"""
    user_id: str
    email: str
    display_name: Optional[str]
    phone_number: Optional[str]
    email_verified: bool
    custom_claims: Dict[str, Any]
    created_at: datetime
    last_sign_in: Optional[datetime]


@dataclass
class CustomClaims:
    """Value Object para claims personalizados"""
    roles: List[str]
    permissions: List[str]
    organization_id: Optional[str] = None


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
    PHONE_NUMBER_EXISTS = "PHONE_NUMBER_EXISTS"
    WEAK_PASSWORD = "WEAK_PASSWORD"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    USER_DISABLED = "USER_DISABLED"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS" 