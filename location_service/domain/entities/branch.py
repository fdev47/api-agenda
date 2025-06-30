"""
Entidad del dominio para sucursales
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Branch(BaseModel):
    """Entidad del dominio para sucursales"""
    id: Optional[int] = Field(None, description="ID de la sucursal")
    name: str = Field(..., description="Nombre de la sucursal")
    code: str = Field(..., description="Código único de la sucursal")
    local_id: int = Field(..., description="ID del local al que pertenece")
    country_id: int = Field(..., description="ID del país")
    state_id: int = Field(..., description="ID del estado")
    city_id: int = Field(..., description="ID de la ciudad")
    address: Optional[str] = Field(None, description="Dirección específica de la sucursal")
    ramps: int = Field(0, description="Número de rampas")
    is_active: bool = Field(True, description="Estado activo de la sucursal")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

    class Config:
        from_attributes = True 