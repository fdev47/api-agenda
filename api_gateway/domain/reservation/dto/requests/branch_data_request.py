"""
DTO de request para datos de sucursal en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional


class BranchDataRequest(BaseModel):
    """DTO para datos de sucursal"""
    # ID de referencia en location_service
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    # Datos completos al momento de la reserva
    name: str = Field(..., min_length=2, max_length=100, description="Nombre de la sucursal")
    code: str = Field(..., min_length=1, max_length=20, description="Código de la sucursal")
    address: str = Field(..., min_length=10, max_length=200, description="Dirección de la sucursal")
    country_id: int = Field(..., gt=0, description="ID del país")
    country_name: str = Field(..., min_length=2, max_length=50, description="Nombre del país")
    state_id: int = Field(..., gt=0, description="ID del estado")
    state_name: str = Field(..., min_length=2, max_length=50, description="Nombre del estado")
    city_id: int = Field(..., gt=0, description="ID de la ciudad")
    city_name: str = Field(..., min_length=2, max_length=50, description="Nombre de la ciudad")
    ramp_id: int = Field(..., gt=0, description="ID de la rampa")
    ramp_name: str = Field(..., min_length=2, max_length=100, description="Nombre de la rampa") 