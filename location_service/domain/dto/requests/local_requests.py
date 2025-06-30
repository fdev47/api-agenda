"""
DTOs de requests para locales
"""
from typing import Optional
from pydantic import BaseModel, Field, validator


class CreateLocalRequest(BaseModel):
    """Request para crear un local"""
    name: str = Field(..., min_length=1, max_length=255, description="Nombre del local")
    code: str = Field(..., min_length=1, max_length=50, description="Código único del local")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del local")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono del local")
    email: Optional[str] = Field(None, max_length=255, description="Email del local")
    is_active: bool = Field(True, description="Estado activo del local")

    @validator('code')
    def validate_code(cls, v):
        if not v.strip():
            raise ValueError('El código no puede estar vacío')
        return v.strip().upper()

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('El email debe tener un formato válido')
        return v


class UpdateLocalRequest(BaseModel):
    """Request para actualizar un local"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombre del local")
    code: Optional[str] = Field(None, min_length=1, max_length=50, description="Código único del local")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del local")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono del local")
    email: Optional[str] = Field(None, max_length=255, description="Email del local")
    is_active: Optional[bool] = Field(None, description="Estado activo del local")

    @validator('code')
    def validate_code(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El código no puede estar vacío')
        return v.strip().upper() if v else v

    @validator('name')
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip() if v else v

    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('El email debe tener un formato válido')
        return v


class LocalFilterRequest(BaseModel):
    """Request para filtrar locales"""
    name: Optional[str] = Field(None, description="Filtrar por nombre")
    code: Optional[str] = Field(None, description="Filtrar por código")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    limit: int = Field(100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(0, ge=0, description="Offset para paginación") 