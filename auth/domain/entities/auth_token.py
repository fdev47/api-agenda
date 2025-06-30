"""
Entidad AuthToken del dominio
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class AuthToken(BaseModel):
    """Entidad AuthToken del dominio de autenticación"""
    model_config = ConfigDict(from_attributes=True)
    
    access_token: str = Field(..., description="Token de acceso")
    refresh_token: Optional[str] = Field(None, description="Token de refresco")
    expires_at: datetime = Field(..., description="Fecha de expiración")
    token_type: str = Field(default="Bearer", description="Tipo de token") 