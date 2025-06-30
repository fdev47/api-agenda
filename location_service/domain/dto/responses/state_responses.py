"""
DTOs de responses para estados
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class StateResponse(BaseModel):
    """Response para un estado"""
    id: int = Field(..., description="ID del estado")
    name: str = Field(..., description="Nombre del estado/provincia")
    code: str = Field(..., description="Código del estado")
    country_id: int = Field(..., description="ID del país al que pertenece")
    country_name: str = Field(..., description="Nombre del país")
    is_active: bool = Field(..., description="Estado activo del estado")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True

class StateListResponse(BaseModel):
    """Response para lista de estados"""
    states: List[StateResponse] = Field(..., description="Lista de estados")
    total: int = Field(..., description="Total de estados")
    limit: int = Field(..., description="Límite de resultados")
    offset: int = Field(..., description="Offset para paginación")

class StateCreatedResponse(BaseModel):
    """Response para estado creado"""
    id: int = Field(..., description="ID del estado creado")
    message: str = Field("Estado creado exitosamente", description="Mensaje de confirmación")

class StateUpdatedResponse(BaseModel):
    """Response para estado actualizado"""
    id: int = Field(..., description="ID del estado actualizado")
    message: str = Field("Estado actualizado exitosamente", description="Mensaje de confirmación")

class StateDeletedResponse(BaseModel):
    """Response para estado eliminado"""
    id: int = Field(..., description="ID del estado eliminado")
    message: str = Field("Estado eliminado exitosamente", description="Mensaje de confirmación") 