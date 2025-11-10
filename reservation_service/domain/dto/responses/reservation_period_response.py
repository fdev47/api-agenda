"""
Response DTO para obtener reservas por período
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


class ReservationPeriodItem(BaseModel):
    """Item de reserva en el período"""
    
    reservation_id: int = Field(..., description="ID de la reserva")
    start_time: datetime = Field(..., description="Fecha y hora de inicio de la reserva")
    end_time: datetime = Field(..., description="Fecha y hora de fin de la reserva")
    
    model_config = ConfigDict(from_attributes=True)


class ReservationPeriodResponse(BaseModel):
    """Response con lista de reservas en el período"""
    
    reservations: List[ReservationPeriodItem] = Field(default_factory=list, description="Lista de reservas")
    total: int = Field(..., description="Total de reservas encontradas")
    
    model_config = ConfigDict(from_attributes=True)

