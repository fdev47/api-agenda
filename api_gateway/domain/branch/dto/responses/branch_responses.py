"""
DTOs de respuestas para sucursales
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class RampSummaryResponse(BaseModel):
    """Resumen de rampa para incluir en respuesta de sucursal"""
    id: int = Field(..., description="ID de la rampa")
    name: str = Field(..., description="Nombre de la rampa")
    is_available: bool = Field(..., description="Disponibilidad de la rampa")


class SectorSummaryResponse(BaseModel):
    """Resumen de sector para incluir en respuesta de sucursal"""
    id: int = Field(..., description="ID del sector")
    name: str = Field(..., description="Nombre del sector")
    sector_type_id: int = Field(..., description="ID del tipo de sector")


class BranchResponse(BaseModel):
    """Response para una sucursal"""
    id: int = Field(..., description="ID de la sucursal")
    name: str = Field(..., description="Nombre de la sucursal")
    code: str = Field(..., description="Código único de la sucursal")
    local_id: int = Field(..., description="ID del local al que pertenece")
    local_name: str = Field(..., description="Nombre del local")
    local_phone: Optional[str] = Field(None, description="Teléfono del local")
    local_email: Optional[str] = Field(None, description="Email del local")
    country_id: int = Field(..., description="ID del país")
    country_name: str = Field(..., description="Nombre del país")
    state_id: int = Field(..., description="ID del estado")
    state_name: str = Field(..., description="Nombre del estado")
    city_id: int = Field(..., description="ID de la ciudad")
    city_name: str = Field(..., description="Nombre de la ciudad")
    address: Optional[str] = Field(None, description="Dirección específica de la sucursal")
    ramps: List[RampSummaryResponse] = Field(default_factory=list, description="Lista de rampas")
    sectors: List[SectorSummaryResponse] = Field(default_factory=list, description="Lista de sectores")
    is_active: bool = Field(..., description="Estado activo de la sucursal")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True


class BranchListResponse(BaseModel):
    """Response para lista de sucursales"""
    branches: List[BranchResponse] = Field(..., description="Lista de sucursales")
    total: int = Field(..., description="Total de sucursales")
    limit: int = Field(..., description="Límite de resultados")
    offset: int = Field(..., description="Offset para paginación")


class BranchCreatedResponse(BaseModel):
    """Response para sucursal creada"""
    id: int = Field(..., description="ID de la sucursal creada")
    message: str = Field("Sucursal creada exitosamente", description="Mensaje de confirmación")


class BranchUpdatedResponse(BaseModel):
    """Response para sucursal actualizada"""
    id: int = Field(..., description="ID de la sucursal actualizada")
    message: str = Field("Sucursal actualizada exitosamente", description="Mensaje de confirmación")


class BranchDeletedResponse(BaseModel):
    """Response para sucursal eliminada"""
    id: int = Field(..., description="ID de la sucursal eliminada")
    message: str = Field("Sucursal eliminada exitosamente", description="Mensaje de confirmación") 