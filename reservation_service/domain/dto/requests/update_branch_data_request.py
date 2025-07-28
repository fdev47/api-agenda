"""
Request DTO para actualización parcial de datos de sucursal
"""
from pydantic import BaseModel, Field
from typing import Optional


class UpdateBranchDataRequest(BaseModel):
    """Request para actualización parcial de datos de la sucursal"""
    # Todos los campos son opcionales para permitir actualización granular
    branch_id: Optional[int] = Field(None, gt=0, description="ID de la sucursal")
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nombre de la sucursal")
    code: Optional[str] = Field(None, min_length=1, max_length=20, description="Código de la sucursal")
    address: Optional[str] = Field(None, max_length=200, description="Dirección de la sucursal")
    country_id: Optional[int] = Field(None, gt=0, description="ID del país")
    country_name: Optional[str] = Field(None, min_length=2, max_length=50, description="Nombre del país")
    state_id: Optional[int] = Field(None, gt=0, description="ID del estado")
    state_name: Optional[str] = Field(None, min_length=2, max_length=50, description="Nombre del estado")
    city_id: Optional[int] = Field(None, gt=0, description="ID de la ciudad")
    city_name: Optional[str] = Field(None, min_length=2, max_length=50, description="Nombre de la ciudad") 