"""
Response DTO para datos de sucursal
"""
from pydantic import BaseModel, Field


class BranchDataResponse(BaseModel):
    """Response para datos de la sucursal"""
    # ID de referencia en location_service
    branch_id: int = Field(..., description="ID de la sucursal")
    # Datos completos al momento de la reserva
    name: str = Field(..., description="Nombre de la sucursal")
    code: str = Field(..., description="Código de la sucursal")
    address: str = Field(..., description="Dirección de la sucursal")
    country_id: int = Field(..., description="ID del país")
    country_name: str = Field(..., description="Nombre del país")
    state_id: int = Field(..., description="ID del estado")
    state_name: str = Field(..., description="Nombre del estado")
    city_id: int = Field(..., description="ID de la ciudad")
    city_name: str = Field(..., description="Nombre de la ciudad")
    ramp_id: int = Field(..., description="ID de la rampa")
    ramp_name: str = Field(..., description="Nombre de la rampa") 