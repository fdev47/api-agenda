"""
Entidad UserCredentials del dominio
"""
from pydantic import BaseModel, Field, ConfigDict


class UserCredentials(BaseModel):
    """Entidad UserCredentials del dominio de autenticación"""
    model_config = ConfigDict(from_attributes=True)
    
    email: str = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña del usuario") 