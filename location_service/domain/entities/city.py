"""
Entidad del dominio para ciudades
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class City(BaseModel):
    """Entidad del dominio para ciudades"""
    id: Optional[int] = Field(None, description="ID de la ciudad")
    name: str = Field(..., description="Nombre de la ciudad")
    code: str = Field(..., description="Código de la ciudad")
    state_id: int = Field(..., description="ID del estado al que pertenece")
    is_active: bool = Field(True, description="Estado activo de la ciudad")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

    class Config:
        from_attributes = True 