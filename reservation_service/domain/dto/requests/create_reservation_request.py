"""
Request DTO para crear reserva
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

from .customer_data_request import CustomerDataRequest
from .branch_data_request import BranchDataRequest
from .sector_data_with_ramp_request import SectorDataWithRampRequest


class CreateReservationRequest(BaseModel):
    """Request para crear una reserva completa"""
    
    # Datos del usuario
    user_id: int = Field(..., gt=0, description="ID del usuario que hace la reserva")
    customer_id: Optional[int] = Field(None, gt=0, description="ID del cliente en el sistema")
    
    # Datos de la sucursal (completos)
    branch_data: BranchDataRequest = Field(..., description="Datos completos de la sucursal")
    
    # Array de sectores con rampa (se crearán main_reservations)
    sector_data: List[SectorDataWithRampRequest] = Field(..., min_items=1, description="Lista de sectores con rampa")
    
    # Datos del cliente (completos)
    customer_data: CustomerDataRequest = Field(..., description="Datos completos del cliente")
    
    # Información de la mercadería
    unloading_time_minutes: int = Field(..., gt=0, le=1440, description="Tiempo de descarga en minutos (máximo 24 horas)")
    reason: str = Field(..., min_length=10, max_length=500, description="Motivo de la reserva")
    cargo_type: Optional[str] = Field(None, max_length=100, description="Tipo de carga")
    
    # Horario de la reserva
    reservation_date: datetime = Field(..., description="Fecha de la reserva")
    start_time: datetime = Field(..., description="Hora de inicio de la reserva")
    end_time: datetime = Field(..., description="Hora de fin de la reserva")
    
    # Información adicional
    notes: Optional[str] = Field(None, max_length=1000, description="Notas adicionales")
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        """Validar que el horario de fin sea posterior al de inicio"""
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError("El horario de fin debe ser posterior al de inicio")
        return v
    
    @validator('reservation_date')
    def validate_reservation_date(cls, v):
        """Validar que la fecha de reserva no sea en el pasado"""
        if v < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            raise ValueError("La fecha de reserva no puede ser en el pasado")
        return v 