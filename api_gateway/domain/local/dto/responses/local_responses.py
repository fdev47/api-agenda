"""
DTOs de respuestas para locales
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class LocalResponse(BaseModel):
    """Response para un local"""
    id: int = Field(..., description="ID del local")
    name: str = Field(..., description="Nombre del local")
    code: str = Field(..., description="Código único del local")
    description: Optional[str] = Field(None, description="Descripción del local")
    phone: Optional[str] = Field(None, description="Teléfono del local")
    email: Optional[str] = Field(None, description="Email del local")
    is_active: bool = Field(..., description="Estado activo del local")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True


class LocalListResponse(BaseModel):
    """Response para lista de locales"""
    locals: List[LocalResponse] = Field(..., description="Lista de locales")
    total: int = Field(..., description="Total de locales")
    limit: int = Field(..., description="Límite de resultados")
    offset: int = Field(..., description="Offset para paginación")


class LocalCreatedResponse(BaseModel):
    """Response para local creado"""
    id: int = Field(..., description="ID del local creado")
    message: str = Field("Local creado exitosamente", description="Mensaje de confirmación")


class LocalUpdatedResponse(BaseModel):
    """Response para local actualizado"""
    id: int = Field(..., description="ID del local actualizado")
    message: str = Field("Local actualizado exitosamente", description="Mensaje de confirmación")


class LocalDeletedResponse(BaseModel):
    """Response para local eliminado"""
    id: int = Field(..., description="ID del local eliminado")
    message: str = Field("Local eliminado exitosamente", description="Mensaje de confirmación") 