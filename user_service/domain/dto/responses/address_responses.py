"""
DTOs de respuesta para Address
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class AddressLocationDetails(BaseModel):
    """Detalles de ubicación obtenidos del location_service"""
    country: Optional[Dict[str, Any]] = Field(None, description="Datos del país")
    state: Optional[Dict[str, Any]] = Field(None, description="Datos del estado")
    city: Optional[Dict[str, Any]] = Field(None, description="Datos de la ciudad")


class AddressResponse(BaseModel):
    """Respuesta de dirección con detalles de ubicación"""
    id: UUID = Field(..., description="ID de la dirección")
    street: str = Field(..., description="Calle y número")
    city_id: UUID = Field(..., description="ID de la ciudad")
    state_id: UUID = Field(..., description="ID del estado")
    country_id: UUID = Field(..., description="ID del país")
    postal_code: Optional[str] = Field(None, description="Código postal")
    additional_info: Optional[str] = Field(None, description="Información adicional")
    
    # Detalles de ubicación (opcional, se puede incluir o no)
    location_details: Optional[AddressLocationDetails] = Field(None, description="Detalles de ubicación")


class AddressListResponse(BaseModel):
    """Respuesta de lista de direcciones"""
    addresses: list[AddressResponse] = Field(..., description="Lista de direcciones")
    total: int = Field(..., description="Total de direcciones")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de la página") 