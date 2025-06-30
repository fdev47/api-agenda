"""
DTOs de responses para países
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CountryResponse(BaseModel):
    """Response para un país"""
    id: int = Field(..., description="ID del país")
    name: str = Field(..., description="Nombre del país")
    code: str = Field(..., description="Código ISO del país")
    phone_code: Optional[str] = Field(None, description="Código de teléfono del país")
    is_active: bool = Field(..., description="Estado activo del país")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True

class CountryListResponse(BaseModel):
    """Response para lista de países"""
    countries: List[CountryResponse] = Field(..., description="Lista de países")
    total: int = Field(..., description="Total de países")
    limit: int = Field(..., description="Límite de resultados")
    offset: int = Field(..., description="Offset para paginación")

class CountryCreatedResponse(BaseModel):
    """Response para país creado"""
    id: int = Field(..., description="ID del país creado")
    message: str = Field("País creado exitosamente", description="Mensaje de confirmación")

class CountryUpdatedResponse(BaseModel):
    """Response para país actualizado"""
    id: int = Field(..., description="ID del país actualizado")
    message: str = Field("País actualizado exitosamente", description="Mensaje de confirmación")

class CountryDeletedResponse(BaseModel):
    """Response para país eliminado"""
    id: int = Field(..., description="ID del país eliminado")
    message: str = Field("País eliminado exitosamente", description="Mensaje de confirmación") 