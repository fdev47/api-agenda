"""
DTOs de responses para ciudades
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CityResponse(BaseModel):
    """Response para una ciudad"""
    id: int = Field(..., description="ID de la ciudad")
    name: str = Field(..., description="Nombre de la ciudad")
    code: Optional[str] = Field(None, description="Código de la ciudad")
    state_id: int = Field(..., description="ID del estado al que pertenece")
    state_name: str = Field(..., description="Nombre del estado")
    country_id: int = Field(..., description="ID del país")
    country_name: str = Field(..., description="Nombre del país")
    is_active: bool = Field(..., description="Estado activo de la ciudad")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True

class CityListResponse(BaseModel):
    """Response para lista de ciudades"""
    cities: List[CityResponse] = Field(..., description="Lista de ciudades")
    total: int = Field(..., description="Total de ciudades")
    limit: int = Field(..., description="Límite de resultados")
    offset: int = Field(..., description="Offset para paginación")

class CityCreatedResponse(BaseModel):
    """Response para ciudad creada"""
    id: int = Field(..., description="ID de la ciudad creada")
    message: str = Field("Ciudad creada exitosamente", description="Mensaje de confirmación")

class CityUpdatedResponse(BaseModel):
    """Response para ciudad actualizada"""
    id: int = Field(..., description="ID de la ciudad actualizada")
    message: str = Field("Ciudad actualizada exitosamente", description="Mensaje de confirmación")

class CityDeletedResponse(BaseModel):
    """Response para ciudad eliminada"""
    id: int = Field(..., description="ID de la ciudad eliminada")
    message: str = Field("Ciudad eliminada exitosamente", description="Mensaje de confirmación") 