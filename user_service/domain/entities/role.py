"""
Entidad Role del dominio
"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4

class Role(BaseModel):
    """Entidad Role del dominio de usuarios"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(default_factory=uuid4, description="Identificador único del rol")
    name: str = Field(..., description="Nombre del rol")
    description: str | None = Field(None, description="Descripción del rol") 