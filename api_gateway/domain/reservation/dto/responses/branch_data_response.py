"""
DTO de response para datos de sucursal en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional


class BranchDataResponse(BaseModel):
    """DTO para datos de sucursal"""
    branch_id: Optional[int] = Field(None, description="ID de la sucursal")
    name: Optional[str] = Field(None, description="Nombre de la sucursal")
    code: Optional[str] = Field(None, description="Código de la sucursal")
    address: Optional[str] = Field(None, description="Dirección de la sucursal")
    country_id: Optional[int] = Field(None, description="ID del país")
    country_name: Optional[str] = Field(None, description="Nombre del país")
    state_id: Optional[int] = Field(None, description="ID del estado")
    state_name: Optional[str] = Field(None, description="Nombre del estado")
    city_id: Optional[int] = Field(None, description="ID de la ciudad")
    city_name: Optional[str] = Field(None, description="Nombre de la ciudad")
    ramp_id: Optional[int] = Field(None, description="ID de la rampa")
    ramp_name: Optional[str] = Field(None, description="Nombre de la rampa") 