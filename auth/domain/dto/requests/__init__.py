"""
DTOs de requests para el dominio de autenticación
"""
from .auth_requests import LoginRequest, RegisterRequest, RefreshTokenRequest, CreateUserRequest, UpdateUserRequest, ChangePasswordRequest, ChangePasswordByUserIdRequest

__all__ = [
    'LoginRequest',
    'RegisterRequest', 
    'RefreshTokenRequest',
    'CreateUserRequest',
    'UpdateUserRequest',
    'ChangePasswordRequest',
    'ChangePasswordByUserIdRequest'
] 