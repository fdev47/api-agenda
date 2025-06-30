"""
Entidad del dominio para estados
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class State(BaseModel):
    """Entidad del dominio para estados"""
    id: Optional[int] = Field(None, description="ID del estado")
    name: str = Field(..., description="Nombre del estado/provincia")
    code: str = Field(..., description="Código del estado")
    country_id: int = Field(..., description="ID del país al que pertenece")
    is_active: bool = Field(True, description="Estado activo del estado")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

    class Config:
        from_attributes = True 