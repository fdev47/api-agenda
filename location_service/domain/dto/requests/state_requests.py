"""
DTOs de requests para estados
"""
from pydantic import BaseModel, Field
from typing import Optional

class CreateStateRequest(BaseModel):
    """Request para crear un estado"""
    name: str = Field(..., description="Nombre del estado/provincia", min_length=2)
    code: str = Field(..., description="Código del estado", min_length=2, max_length=10)
    country_id: int = Field(..., gt=0, description="ID del país al que pertenece")

class UpdateStateRequest(BaseModel):
    """Request para actualizar un estado"""
    name: Optional[str] = Field(None, description="Nombre del estado/provincia", min_length=2)
    code: Optional[str] = Field(None, description="Código del estado", min_length=2, max_length=10)
    country_id: Optional[int] = Field(None, gt=0, description="ID del país al que pertenece")

class StateFilterRequest(BaseModel):
    """Request para filtrar estados"""
    name: Optional[str] = Field(None, description="Filtrar por nombre")
    code: Optional[str] = Field(None, description="Filtrar por código")
    country_id: Optional[int] = Field(None, description="Filtrar por país")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    limit: int = Field(100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(0, ge=0, description="Offset para paginación") 