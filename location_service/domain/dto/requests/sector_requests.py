"""
DTOs de requests para sectores
"""
from pydantic import BaseModel, Field, validator
from typing import Optional


class CreateSectorRequest(BaseModel):
    """DTO para crear un sector"""
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del sector")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del sector")
    branch_id: int = Field(..., gt=0, description="ID de la sucursal a la que pertenece el sector")
    sector_type_id: int = Field(..., gt=0, description="ID del tipo de sector")
    is_active: bool = Field(True, description="Estado activo del sector")
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre del sector no puede estar vacío')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if v is not None:
            return v.strip() if v.strip() else None
        return v


class UpdateSectorRequest(BaseModel):
    """DTO para actualizar un sector"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del sector")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del sector")
    sector_type_id: Optional[int] = Field(None, gt=0, description="ID del tipo de sector")
    is_active: Optional[bool] = Field(None, description="Estado activo del sector")
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('El nombre del sector no puede estar vacío')
            return v.strip()
        return v
    
    @validator('description')
    def validate_description(cls, v):
        if v is not None:
            return v.strip() if v.strip() else None
        return v


class SectorFilterRequest(BaseModel):
    """DTO para filtrar sectores"""
    name: Optional[str] = Field(None, description="Filtrar por nombre")
    branch_id: Optional[int] = Field(None, gt=0, description="Filtrar por sucursal")
    sector_type_id: Optional[int] = Field(None, gt=0, description="Filtrar por tipo de sector")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    limit: int = Field(100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(0, ge=0, description="Offset para paginación") 