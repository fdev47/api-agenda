"""DTOs de respuesta para API Gateway"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any, Dict


class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    error: str
    message: str
    error_code: str
    timestamp: str
    request_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class UserResponse(BaseModel):
    """Respuesta de usuario"""
    user_id: str
    email: str
    display_name: str
    email_verified: bool
    created_at: str
    last_sign_in: Optional[str] = None
    custom_claims: Optional[Dict[str, Any]] = None


class AuthResponse(BaseModel):
    """Respuesta de autenticación"""
    user: UserResponse
    access_token: str
    refresh_token: str
    expires_in: int


class TokenResponse(BaseModel):
    """Respuesta de token"""
    access_token: str
    refresh_token: str
    expires_in: int


class UserListResponse(BaseModel):
    """Respuesta de lista de usuarios"""
    users: list[UserResponse]
    total: int
    skip: int
    limit: int


class SuccessResponse(BaseModel):
    """Respuesta de éxito genérica"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None 