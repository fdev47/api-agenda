"""
Entidad del dominio para locales
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Local(BaseModel):
    """Entidad del dominio para locales"""
    id: Optional[int] = Field(None, description="ID del local")
    name: str = Field(..., description="Nombre del local")
    code: str = Field(..., description="Código único del local")
    description: Optional[str] = Field(None, description="Descripción del local")
    phone: Optional[str] = Field(None, description="Teléfono del local")
    email: Optional[str] = Field(None, description="Email del local")
    is_active: bool = Field(True, description="Estado activo del local")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

    class Config:
        from_attributes = True 