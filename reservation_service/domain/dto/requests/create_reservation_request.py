"""
Request DTO para crear reserva
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

from .order_number_request import OrderNumberRequest
from .customer_data_request import CustomerDataRequest
from .branch_data_request import BranchDataRequest
from .sector_data_request import SectorDataRequest


class CreateReservationRequest(BaseModel):
    """Request para crear una reserva completa"""
    
    # Datos del usuario (opcional, puede venir del token)
    user_id: Optional[int] = Field(None, gt=0, description="ID del usuario que hace la reserva")
    customer_id: Optional[int] = Field(None, gt=0, description="ID del cliente en el sistema")
    
    # Datos de la sucursal (completos)
    branch_data: BranchDataRequest = Field(..., description="Datos completos de la sucursal")
    
    # Datos del sector (completos)
    sector_data: SectorDataRequest = Field(..., description="Datos completos del sector")
    
    # Datos del cliente (completos)
    customer_data: CustomerDataRequest = Field(..., description="Datos completos del cliente")
    
    # Información de la mercadería
    unloading_time_minutes: int = Field(..., gt=0, le=1440, description="Tiempo de descarga en minutos (máximo 24 horas)")
    reason: str = Field(..., min_length=10, max_length=500, description="Motivo de la reserva")
    
    # Números de pedidos
    order_numbers: List[OrderNumberRequest] = Field(..., min_items=1, max_items=50, description="Lista de números de pedido")
    
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