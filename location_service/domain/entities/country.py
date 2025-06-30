"""
Entidad del dominio para países
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Country(BaseModel):
    """Entidad del dominio para países"""
    id: Optional[int] = Field(None, description="ID del país")
    name: str = Field(..., description="Nombre del país")
    code: str = Field(..., description="Código ISO del país")
    phone_code: Optional[str] = Field(None, description="Código de teléfono del país")
    is_active: bool = Field(True, description="Estado activo del país")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

    class Config:
        from_attributes = True 