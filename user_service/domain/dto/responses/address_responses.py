"""
DTOs de responses para Address
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class AddressResponse(BaseModel):
    """Response para una dirección"""
    id: UUID = Field(..., description="Identificador único de la dirección")
    street: str = Field(..., description="Calle y número")
    city_id: int = Field(..., description="ID de la ciudad")
    state_id: int = Field(..., description="ID del estado")
    country_id: int = Field(..., description="ID del país")
    postal_code: Optional[str] = Field(None, description="Código postal")
    additional_info: Optional[str] = Field(None, description="Información adicional")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True


class AddressListResponse(BaseModel):
    """Response para lista de direcciones"""
    addresses: List[AddressResponse] = Field(..., description="Lista de direcciones")
    total: int = Field(..., description="Total de direcciones")


class AddressCreatedResponse(BaseModel):
    """Response para dirección creada"""
    id: UUID = Field(..., description="ID de la dirección creada")
    message: str = Field("Dirección creada exitosamente", description="Mensaje de confirmación")


class AddressUpdatedResponse(BaseModel):
    """Response para dirección actualizada"""
    id: UUID = Field(..., description="ID de la dirección actualizada")
    message: str = Field("Dirección actualizada exitosamente", description="Mensaje de confirmación")


class AddressDeletedResponse(BaseModel):
    """Response para dirección eliminada"""
    id: UUID = Field(..., description="ID de la dirección eliminada")
    message: str = Field("Dirección eliminada exitosamente", description="Mensaje de confirmación") 