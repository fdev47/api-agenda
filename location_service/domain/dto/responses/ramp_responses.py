"""
DTOs de responses para rampas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class RampResponse(BaseModel):
    """DTO para respuesta de rampa"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID de la rampa")
    name: str = Field(..., description="Nombre de la rampa")
    is_available: bool = Field(..., description="Indica si la rampa está disponible")
    branch_id: int = Field(..., description="ID de la sucursal")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")


class RampListResponse(BaseModel):
    """DTO para lista de rampas"""
    ramps: List[RampResponse] = Field(..., description="Lista de rampas")
    total: int = Field(..., description="Total de rampas")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de la página")


class RampCreatedResponse(BaseModel):
    """DTO para respuesta de rampa creada"""
    id: int = Field(..., description="ID de la rampa creada")
    name: str = Field(..., description="Nombre de la rampa")
    is_available: bool = Field(..., description="Indica si la rampa está disponible")
    branch_id: int = Field(..., description="ID de la sucursal")
    message: str = Field(default="Rampa creada exitosamente", description="Mensaje de confirmación")


class RampUpdatedResponse(BaseModel):
    """DTO para respuesta de rampa actualizada"""
    id: int = Field(..., description="ID de la rampa")
    name: str = Field(..., description="Nombre de la rampa")
    is_available: bool = Field(..., description="Indica si la rampa está disponible")
    branch_id: int = Field(..., description="ID de la sucursal")
    message: str = Field(default="Rampa actualizada exitosamente", description="Mensaje de confirmación")


class RampDeletedResponse(BaseModel):
    """DTO para respuesta de rampa eliminada"""
    id: int = Field(..., description="ID de la rampa eliminada")
    message: str = Field(default="Rampa eliminada exitosamente", description="Mensaje de confirmación") 