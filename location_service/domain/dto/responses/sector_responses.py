"""
DTOs de responses para sectores
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class SectorResponse(BaseModel):
    """DTO para respuesta de sector"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID del sector")
    name: str = Field(..., description="Nombre del sector")
    description: Optional[str] = Field(None, description="Descripción del sector")
    branch_id: int = Field(..., description="ID de la sucursal")
    sector_type_id: int = Field(..., description="ID del tipo de sector")
    measurement_unit: Optional[str] = Field(None, description="Unidad de medida del sector")
    is_active: bool = Field(..., description="Estado activo del sector")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")


class SectorListResponse(BaseModel):
    """DTO para lista de sectores"""
    sectors: List[SectorResponse] = Field(..., description="Lista de sectores")
    total: int = Field(..., description="Total de sectores")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de la página")


class SectorCreatedResponse(BaseModel):
    """DTO para respuesta de sector creado"""
    id: int = Field(..., description="ID del sector creado")
    name: str = Field(..., description="Nombre del sector")
    description: Optional[str] = Field(None, description="Descripción del sector")
    branch_id: int = Field(..., description="ID de la sucursal")
    sector_type_id: int = Field(..., description="ID del tipo de sector")
    measurement_unit: Optional[str] = Field(None, description="Unidad de medida del sector")
    is_active: bool = Field(..., description="Estado activo del sector")
    message: str = Field(default="Sector creado exitosamente", description="Mensaje de confirmación")


class SectorUpdatedResponse(BaseModel):
    """DTO para respuesta de sector actualizado"""
    id: int = Field(..., description="ID del sector")
    name: str = Field(..., description="Nombre del sector")
    description: Optional[str] = Field(None, description="Descripción del sector")
    branch_id: int = Field(..., description="ID de la sucursal")
    sector_type_id: int = Field(..., description="ID del tipo de sector")
    measurement_unit: Optional[str] = Field(None, description="Unidad de medida del sector")
    is_active: bool = Field(..., description="Estado activo del sector")
    message: str = Field(default="Sector actualizado exitosamente", description="Mensaje de confirmación")


class SectorDeletedResponse(BaseModel):
    """DTO para respuesta de sector eliminado"""
    id: int = Field(..., description="ID del sector eliminado")
    message: str = Field(default="Sector eliminado exitosamente", description="Mensaje de confirmación") 