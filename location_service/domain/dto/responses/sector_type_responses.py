"""
DTOs de responses para tipos de sector
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class SectorTypeResponse(BaseModel):
    """DTO para respuesta de tipo de sector"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID del tipo de sector")
    name: str = Field(..., description="Nombre del tipo de sector")
    code: str = Field(..., description="Código del tipo de sector")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")


class SectorTypeListResponse(BaseModel):
    """DTO para lista de tipos de sector"""
    sector_types: List[SectorTypeResponse] = Field(..., description="Lista de tipos de sector")
    total: int = Field(..., description="Total de tipos de sector")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de la página")


class SectorTypeCreatedResponse(BaseModel):
    """DTO para respuesta de tipo de sector creado"""
    id: int = Field(..., description="ID del tipo de sector creado")
    name: str = Field(..., description="Nombre del tipo de sector")
    code: str = Field(..., description="Código del tipo de sector")
    message: str = Field(default="Tipo de sector creado exitosamente", description="Mensaje de confirmación")


class SectorTypeUpdatedResponse(BaseModel):
    """DTO para respuesta de tipo de sector actualizado"""
    id: int = Field(..., description="ID del tipo de sector")
    name: str = Field(..., description="Nombre del tipo de sector")
    code: str = Field(..., description="Código del tipo de sector")
    message: str = Field(default="Tipo de sector actualizado exitosamente", description="Mensaje de confirmación")


class SectorTypeDeletedResponse(BaseModel):
    """DTO para respuesta de tipo de sector eliminado"""
    id: int = Field(..., description="ID del tipo de sector eliminado")
    message: str = Field(default="Tipo de sector eliminado exitosamente", description="Mensaje de confirmación") 