"""
DTO de response para main_reservation en el API Gateway
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from .sector_data_response import SectorDataResponse


class MainReservationResponse(BaseModel):
    """DTO de respuesta para main_reservation"""
    id: int = Field(..., description="ID de la main_reservation")
    sector_id: int = Field(..., description="ID del sector")
    reservation_id: int = Field(..., description="ID de la reserva principal")
    sector_data: SectorDataResponse = Field(..., description="Datos completos del sector (incluye ramp_id y ramp_name)")
    reservation_date: datetime = Field(..., description="Fecha de la reserva")
    start_time: datetime = Field(..., description="Hora de inicio")
    end_time: datetime = Field(..., description="Hora de fin")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True

