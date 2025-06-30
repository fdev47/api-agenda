"""
DTOs de requests para sucursales
"""
from typing import Optional
from pydantic import BaseModel, Field, validator


class CreateBranchRequest(BaseModel):
    """Request para crear una sucursal"""
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la sucursal")
    code: str = Field(..., min_length=1, max_length=50, description="Código único de la sucursal")
    local_id: int = Field(..., gt=0, description="ID del local al que pertenece")
    country_id: int = Field(..., gt=0, description="ID del país")
    state_id: int = Field(..., gt=0, description="ID del estado")
    city_id: int = Field(..., gt=0, description="ID de la ciudad")
    address: Optional[str] = Field(None, max_length=255, description="Dirección específica de la sucursal")
    ramps: int = Field(0, ge=0, description="Número de rampas")
    is_active: bool = Field(True, description="Estado activo de la sucursal")

    @validator('code')
    def validate_code(cls, v):
        if not v.strip():
            raise ValueError('El código no puede estar vacío')
        return v.strip().upper()

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()


class UpdateBranchRequest(BaseModel):
    """Request para actualizar una sucursal"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombre de la sucursal")
    code: Optional[str] = Field(None, min_length=1, max_length=50, description="Código único de la sucursal")
    local_id: Optional[int] = Field(None, gt=0, description="ID del local al que pertenece")
    country_id: Optional[int] = Field(None, gt=0, description="ID del país")
    state_id: Optional[int] = Field(None, gt=0, description="ID del estado")
    city_id: Optional[int] = Field(None, gt=0, description="ID de la ciudad")
    address: Optional[str] = Field(None, max_length=255, description="Dirección específica de la sucursal")
    ramps: Optional[int] = Field(None, ge=0, description="Número de rampas")
    is_active: Optional[bool] = Field(None, description="Estado activo de la sucursal")

    @validator('code')
    def validate_code(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El código no puede estar vacío')
        return v.strip().upper() if v else v

    @validator('name')
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip() if v else v


class BranchFilterRequest(BaseModel):
    """Request para filtrar sucursales"""
    name: Optional[str] = Field(None, description="Filtrar por nombre")
    code: Optional[str] = Field(None, description="Filtrar por código")
    local_id: Optional[int] = Field(None, description="Filtrar por local")
    country_id: Optional[int] = Field(None, description="Filtrar por país")
    state_id: Optional[int] = Field(None, description="Filtrar por estado")
    city_id: Optional[int] = Field(None, description="Filtrar por ciudad")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    limit: int = Field(100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(0, ge=0, description="Offset para paginación") 