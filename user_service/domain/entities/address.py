"""
Entidad Address del dominio
"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
from typing import Optional

class Address(BaseModel):
    """Entidad Address del dominio"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(default_factory=uuid4, description="Identificador único de la dirección")
    street: str = Field(..., description="Calle y número")
    city_id: UUID = Field(..., description="ID de la ciudad")
    state_id: UUID = Field(..., description="ID del estado")
    country_id: UUID = Field(..., description="ID del país")
    postal_code: Optional[str] = Field(None, description="Código postal")
    additional_info: Optional[str] = Field(None, description="Información adicional (referencias, etc.)") 