"""
Request DTO para actualizar reserva
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

from .order_number_request import OrderNumberRequest


class UpdateReservationRequest(BaseModel):
    """Request para actualizar una reserva"""
    
    # Campos opcionales para actualización
    unloading_time_minutes: Optional[int] = Field(None, gt=0, le=1440)
    reason: Optional[str] = Field(None, min_length=10, max_length=500)
    order_numbers: Optional[List[OrderNumberRequest]] = Field(None, min_items=1, max_items=50)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=1000)
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        """Validar que el horario de fin sea posterior al de inicio"""
        if v and 'start_time' in values and values['start_time'] and v <= values['start_time']:
            raise ValueError("El horario de fin debe ser posterior al de inicio")
        return v 