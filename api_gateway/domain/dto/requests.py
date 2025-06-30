"""DTOs de request para API Gateway"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    """Request para login de usuario"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")


class RegisterRequest(BaseModel):
    """Request para registro de usuario"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")
    display_name: str = Field(..., min_length=2, description="Nombre completo del usuario")


class RefreshTokenRequest(BaseModel):
    """Request para refresh de token"""
    refresh_token: str = Field(..., description="Token de refresh")


class CreateUserRequest(BaseModel):
    """Request para crear usuario"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")
    display_name: str = Field(..., min_length=2, description="Nombre completo del usuario")


class UpdateUserRequest(BaseModel):
    """Request para actualizar usuario"""
    display_name: Optional[str] = Field(None, min_length=2, description="Nombre completo del usuario")
    email_verified: Optional[bool] = Field(None, description="Estado de verificación de email") 