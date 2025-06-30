"""
DTOs de requests para tipos de sector
"""
from pydantic import BaseModel, Field, validator
from typing import Optional


class CreateSectorTypeRequest(BaseModel):
    """DTO para crear un tipo de sector"""
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del tipo de sector")
    code: str = Field(..., min_length=1, max_length=20, description="Código único del tipo de sector")
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre del tipo de sector no puede estar vacío')
        return v.strip()
    
    @validator('code')
    def validate_code(cls, v):
        if not v or not v.strip():
            raise ValueError('El código del tipo de sector no puede estar vacío')
        return v.strip().upper()


class UpdateSectorTypeRequest(BaseModel):
    """DTO para actualizar un tipo de sector"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del tipo de sector")
    code: Optional[str] = Field(None, min_length=1, max_length=20, description="Código único del tipo de sector")
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('El nombre del tipo de sector no puede estar vacío')
            return v.strip()
        return v
    
    @validator('code')
    def validate_code(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('El código del tipo de sector no puede estar vacío')
            return v.strip().upper()
        return v


class SectorTypeFilterRequest(BaseModel):
    """DTO para filtrar tipos de sector"""
    name: Optional[str] = Field(None, description="Filtrar por nombre")
    code: Optional[str] = Field(None, description="Filtrar por código")
    limit: int = Field(100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(0, ge=0, description="Offset para paginación") 