"""
Entidad UserRegistration del dominio
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class UserRegistration(BaseModel):
    """Entidad UserRegistration del dominio de autenticación"""
    model_config = ConfigDict(from_attributes=True)
    
    email: str = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña del usuario")
    display_name: Optional[str] = Field(None, description="Nombre para mostrar")
    phone_number: Optional[str] = Field(None, description="Número de teléfono") 