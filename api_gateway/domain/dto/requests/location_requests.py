"""
DTOs de requests para location en el API Gateway
"""
from typing import Optional
from pydantic import BaseModel, Field


class MeasurementUnitFilterRequest(BaseModel):
    """Request para filtrar unidades de medida"""
    name: Optional[str] = Field(None, description="Filtrar por nombre")
    code: Optional[str] = Field(None, description="Filtrar por código")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    limit: int = Field(default=100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(default=0, ge=0, description="Offset para paginación")


class SectorTypeFilterRequest(BaseModel):
    """Request para filtrar tipos de sector"""
    name: Optional[str] = Field(None, description="Filtrar por nombre")
    code: Optional[str] = Field(None, description="Filtrar por código")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    limit: int = Field(default=100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(default=0, ge=0, description="Offset para paginación") 