"""
DTOs de requests para Address
"""
from pydantic import BaseModel, Field
from typing import Optional


class CreateAddressRequest(BaseModel):
    """Request para crear una dirección"""
    street: str = Field(..., description="Calle y número")
    city_id: int = Field(..., description="ID de la ciudad")
    state_id: int = Field(..., description="ID del estado")
    country_id: int = Field(..., description="ID del país")
    postal_code: Optional[str] = Field(None, description="Código postal")
    additional_info: Optional[str] = Field(None, description="Información adicional")


class UpdateAddressRequest(BaseModel):
    """Request para actualizar una dirección"""
    street: Optional[str] = Field(None, description="Calle y número")
    city_id: Optional[int] = Field(None, description="ID de la ciudad")
    state_id: Optional[int] = Field(None, description="ID del estado")
    country_id: Optional[int] = Field(None, description="ID del país")
    postal_code: Optional[str] = Field(None, description="Código postal")
    additional_info: Optional[str] = Field(None, description="Información adicional") 