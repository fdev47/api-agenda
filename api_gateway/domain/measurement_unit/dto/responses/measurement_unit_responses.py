"""
DTOs de respuestas para unidades de medida
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MeasurementUnitResponse(BaseModel):
    """Response para una unidad de medida"""
    id: int = Field(..., description="ID de la unidad de medida")
    name: str = Field(..., description="Nombre de la unidad de medida")
    code: str = Field(..., description="Código de la unidad de medida")
    description: Optional[str] = Field(None, description="Descripción de la unidad de medida")
    is_active: bool = Field(..., description="Estado activo de la unidad de medida")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

    class Config:
        from_attributes = True


class MeasurementUnitListResponse(BaseModel):
    """Response para lista de unidades de medida"""
    items: List[MeasurementUnitResponse] = Field(..., description="Lista de unidades de medida")
    total: int = Field(..., description="Total de unidades de medida")
    limit: int = Field(..., description="Límite de resultados")
    offset: int = Field(..., description="Offset para paginación")


class MeasurementUnitCreatedResponse(BaseModel):
    """Response para unidad de medida creada"""
    id: int = Field(..., description="ID de la unidad de medida creada")
    name: str = Field(..., description="Nombre de la unidad de medida")
    code: str = Field(..., description="Código de la unidad de medida")
    description: Optional[str] = Field(None, description="Descripción de la unidad de medida")
    is_active: bool = Field(..., description="Estado activo de la unidad de medida")
    created_at: datetime = Field(..., description="Fecha de creación")
    message: str = Field(..., description="Mensaje de confirmación")

    class Config:
        from_attributes = True


class MeasurementUnitUpdatedResponse(BaseModel):
    """Response para unidad de medida actualizada"""
    id: int = Field(..., description="ID de la unidad de medida")
    name: str = Field(..., description="Nombre de la unidad de medida")
    code: str = Field(..., description="Código de la unidad de medida")
    description: Optional[str] = Field(None, description="Descripción de la unidad de medida")
    is_active: bool = Field(..., description="Estado activo de la unidad de medida")
    updated_at: datetime = Field(..., description="Fecha de última actualización")
    message: str = Field(..., description="Mensaje de confirmación")

    class Config:
        from_attributes = True


class MeasurementUnitDeletedResponse(BaseModel):
    """Response para unidad de medida eliminada"""
    id: int = Field(..., description="ID de la unidad de medida eliminada")
    message: str = Field(..., description="Mensaje de confirmación") 