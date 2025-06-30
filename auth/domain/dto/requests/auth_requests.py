"""
DTOs de requests de autenticación
"""
from pydantic import BaseModel, Field, EmailStr
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
    phone_number: Optional[str] = Field(None, description="Número de teléfono")


class RefreshTokenRequest(BaseModel):
    """Request para refrescar token"""
    refresh_token: str = Field(..., description="Token de refresco")


class CreateUserRequest(BaseModel):
    """Request para crear usuario en Firebase (uso interno)"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")
    display_name: str = Field(..., min_length=2, description="Nombre completo del usuario") 