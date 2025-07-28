"""
Request DTO para actualización parcial de datos de sector
"""
from pydantic import BaseModel, Field
from typing import Optional


class UpdateSectorDataRequest(BaseModel):
    """Request para actualización parcial de datos del sector"""
    # Todos los campos son opcionales para permitir actualización granular
    sector_id: Optional[int] = Field(None, gt=0, description="ID del sector")
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nombre del sector")
    description: Optional[str] = Field(None, max_length=200, description="Descripción del sector")
    sector_type_id: Optional[int] = Field(None, gt=0, description="ID del tipo de sector")
    sector_type_name: Optional[str] = Field(None, min_length=2, max_length=50, description="Nombre del tipo de sector")
    capacity: Optional[float] = Field(None, gt=0, description="Capacidad del sector")
    measurement_unit_id: Optional[int] = Field(None, gt=0, description="ID de la unidad de medida")
    measurement_unit_name: Optional[str] = Field(None, min_length=1, max_length=20, description="Nombre de la unidad de medida") 