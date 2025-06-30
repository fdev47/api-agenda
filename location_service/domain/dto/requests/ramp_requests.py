"""
DTOs de requests para rampas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional


class CreateRampRequest(BaseModel):
    """DTO para crear una rampa"""
    name: str = Field(..., min_length=1, max_length=100, description="Nombre de la rampa")
    is_available: bool = Field(default=True, description="Indica si la rampa está disponible")
    branch_id: int = Field(..., gt=0, description="ID de la sucursal a la que pertenece la rampa")
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre de la rampa no puede estar vacío')
        return v.strip()


class UpdateRampRequest(BaseModel):
    """DTO para actualizar una rampa"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre de la rampa")
    is_available: Optional[bool] = Field(None, description="Indica si la rampa está disponible")
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('El nombre de la rampa no puede estar vacío')
            return v.strip()
        return v


class RampFilterRequest(BaseModel):
    """DTO para filtrar rampas"""
    name: Optional[str] = Field(None, description="Filtrar por nombre")
    branch_id: Optional[int] = Field(None, gt=0, description="Filtrar por sucursal")
    is_available: Optional[bool] = Field(None, description="Filtrar por disponibilidad")
    limit: int = Field(100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(0, ge=0, description="Offset para paginación") 