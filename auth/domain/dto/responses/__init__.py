"""
DTOs de responses para el dominio de autenticación
"""
from .auth_responses import AuthResponse, UserInfoResponse, TokenResponse
from .error_responses import ErrorResponse, ValidationErrorResponse, AuthErrorResponse

__all__ = [
    'AuthResponse',
    'UserInfoResponse',
    'TokenResponse',
    'ErrorResponse',
    'ValidationErrorResponse',
    'AuthErrorResponse'
] 