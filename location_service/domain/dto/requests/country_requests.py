"""
DTOs de requests para países
"""
from pydantic import BaseModel, Field
from typing import Optional

class CreateCountryRequest(BaseModel):
    """Request para crear un país"""
    name: str = Field(..., description="Nombre del país", min_length=2)
    code: str = Field(..., description="Código ISO del país", min_length=2, max_length=3)

class UpdateCountryRequest(BaseModel):
    """Request para actualizar un país"""
    name: Optional[str] = Field(None, description="Nombre del país", min_length=2)
    code: Optional[str] = Field(None, description="Código ISO del país", min_length=2, max_length=3)

class CountryFilterRequest(BaseModel):
    """Request para filtrar países"""
    name: Optional[str] = Field(None, description="Filtrar por nombre")
    code: Optional[str] = Field(None, description="Filtrar por código")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    limit: int = Field(100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(0, ge=0, description="Offset para paginación") 