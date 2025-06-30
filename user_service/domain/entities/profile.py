"""
Entidad Profile del dominio
"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
from typing import List
from .role import Role

class Profile(BaseModel):
    """Entidad Profile del dominio de usuarios"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(default_factory=uuid4, description="Identificador único del perfil")
    name: str = Field(..., description="Nombre del perfil")
    description: str | None = Field(None, description="Descripción del perfil")
    roles: List[Role] = Field(default=[], description="Roles del perfil") 