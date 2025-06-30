"""
DTOs de requests para ciudades
"""
from pydantic import BaseModel, Field
from typing import Optional

class CreateCityRequest(BaseModel):
    """Request para crear una ciudad"""
    name: str = Field(..., description="Nombre de la ciudad", min_length=2)
    state_id: int = Field(..., gt=0, description="ID del estado al que pertenece")

class UpdateCityRequest(BaseModel):
    """Request para actualizar una ciudad"""
    name: Optional[str] = Field(None, description="Nombre de la ciudad", min_length=2)
    state_id: Optional[int] = Field(None, gt=0, description="ID del estado al que pertenece")

class CityFilterRequest(BaseModel):
    """Request para filtrar ciudades"""
    name: Optional[str] = Field(None, description="Filtrar por nombre")
    state_id: Optional[int] = Field(None, description="Filtrar por estado")
    country_id: Optional[int] = Field(None, description="Filtrar por país")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    limit: int = Field(100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(0, ge=0, description="Offset para paginación") 