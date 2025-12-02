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
    phone_number: Optional[str] = Field(None, description="Número de teléfono")
    two_factor_enabled: bool = Field(default=False, description="Habilitar autenticación de dos factores")
    send_email_verification: bool = Field(default=True, description="Enviar email de verificación")


class UpdateUserRequest(BaseModel):
    """Request para actualizar usuario en Firebase"""
    email: Optional[EmailStr] = Field(None, description="Email del usuario")
    display_name: Optional[str] = Field(None, description="Nombre completo del usuario")
    phone_number: Optional[str] = Field(None, description="Número de teléfono")
    password: Optional[str] = Field(None, min_length=6, description="Nueva contraseña del usuario")
    two_factor_enabled: Optional[bool] = Field(None, description="Habilitar autenticación de dos factores")
    email_verified: Optional[bool] = Field(None, description="Marcar email como verificado")


class ChangePasswordRequest(BaseModel):
    """Request para cambiar contraseña de usuario"""
    email: EmailStr = Field(..., description="Email del usuario")
    new_password: str = Field(..., min_length=6, description="Nueva contraseña del usuario") 