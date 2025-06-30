"""
Entidad AuthenticatedUser del dominio
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any


class AuthenticatedUser(BaseModel):
    """Entidad AuthenticatedUser del dominio de autenticación"""
    model_config = ConfigDict(from_attributes=True)
    
    user_id: str = Field(..., description="ID del usuario")
    email: str = Field(..., description="Email del usuario")
    display_name: Optional[str] = Field(None, description="Nombre para mostrar")
    phone_number: Optional[str] = Field(None, description="Número de teléfono")
    email_verified: bool = Field(..., description="Email verificado")
    custom_claims: Dict[str, Any] = Field(default_factory=dict, description="Claims personalizados")
    created_at: datetime = Field(..., description="Fecha de creación")
    last_sign_in: Optional[datetime] = Field(None, description="Último inicio de sesión") 