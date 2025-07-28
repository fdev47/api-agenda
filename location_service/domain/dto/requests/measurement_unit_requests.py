"""
DTOs de requests para unidades de medida
"""
from typing import Optional
from pydantic import BaseModel, Field


class CreateMeasurementUnitRequest(BaseModel):
    """Request para crear una unidad de medida"""
    name: str = Field(..., min_length=1, max_length=50, description="Nombre de la unidad de medida")
    code: str = Field(..., min_length=1, max_length=20, description="Código único de la unidad de medida")
    description: Optional[str] = Field(None, max_length=200, description="Descripción de la unidad de medida")
    is_active: bool = Field(default=True, description="Estado activo de la unidad de medida")


class UpdateMeasurementUnitRequest(BaseModel):
    """Request para actualizar una unidad de medida"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Nombre de la unidad de medida")
    code: Optional[str] = Field(None, min_length=1, max_length=20, description="Código único de la unidad de medida")
    description: Optional[str] = Field(None, max_length=200, description="Descripción de la unidad de medida")
    is_active: Optional[bool] = Field(None, description="Estado activo de la unidad de medida")


class MeasurementUnitFilterRequest(BaseModel):
    """Request para filtrar unidades de medida"""
    name: Optional[str] = Field(None, description="Filtrar por nombre")
    code: Optional[str] = Field(None, description="Filtrar por código")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    limit: int = Field(default=100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(default=0, ge=0, description="Offset para paginación") 