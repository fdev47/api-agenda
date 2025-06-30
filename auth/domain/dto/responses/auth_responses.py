"""
DTOs de responses de autenticación
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class TokenResponse(BaseModel):
    """Response con información del token"""
    access_token: str = Field(..., description="Token de acceso")
    refresh_token: Optional[str] = Field(None, description="Token de refresco")
    expires_at: datetime = Field(..., description="Fecha de expiración")
    token_type: str = Field(default="Bearer", description="Tipo de token")


class UserInfoResponse(BaseModel):
    """Response con información del usuario"""
    user_id: str = Field(..., description="ID del usuario")
    email: str = Field(..., description="Email del usuario")
    display_name: Optional[str] = Field(None, description="Nombre para mostrar")
    phone_number: Optional[str] = Field(None, description="Número de teléfono")
    email_verified: bool = Field(..., description="Email verificado")
    custom_claims: Dict[str, Any] = Field(default_factory=dict, description="Claims personalizados")
    created_at: datetime = Field(..., description="Fecha de creación")
    last_sign_in: Optional[datetime] = Field(None, description="Último inicio de sesión")


class AuthResponse(BaseModel):
    """Response completo de autenticación"""
    token: TokenResponse = Field(..., description="Información del token")
    user: UserInfoResponse = Field(..., description="Información del usuario") 