"""
DTO de request para crear main_reservation en el API Gateway
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from .sector_data_request import SectorDataRequest


class CreateMainReservationRequest(BaseModel):
    """DTO para crear main_reservation"""
    sector_id: int = Field(..., gt=0, description="ID del sector")
    reservation_id: int = Field(..., gt=0, description="ID de la reserva principal")
    ramp_id: int = Field(..., gt=0, description="ID de la rampa")
    sector_data: SectorDataRequest = Field(..., description="Datos completos del sector")
    reservation_date: datetime = Field(..., description="Fecha de la reserva")
    start_time: datetime = Field(..., description="Hora de inicio")
    end_time: datetime = Field(..., description="Hora de fin")

