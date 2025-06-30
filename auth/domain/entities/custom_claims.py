"""
Entidad CustomClaims del dominio
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class CustomClaims(BaseModel):
    """Entidad CustomClaims del dominio de autenticación"""
    model_config = ConfigDict(from_attributes=True)
    
    roles: List[str] = Field(default_factory=list, description="Roles del usuario")
    permissions: List[str] = Field(default_factory=list, description="Permisos del usuario")
    organization_id: Optional[str] = Field(None, description="ID de la organización") 