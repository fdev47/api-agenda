"""
DTO de request para actualizar reserva en el API Gateway
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

from .order_number_request import OrderNumberRequest
from .customer_data_request import CustomerDataRequest
from .branch_data_request import BranchDataRequest
from .sector_data_request import SectorDataRequest


class UpdateReservationRequest(BaseModel):
    """Request para actualizar una reserva"""
    
    # Datos del usuario (opcional)
    user_id: Optional[int] = Field(None, gt=0, description="ID del usuario que hace la reserva")
    customer_id: Optional[int] = Field(None, gt=0, description="ID del cliente en el sistema")
    
    # Datos de la sucursal (opcional)
    branch_data: Optional[BranchDataRequest] = Field(None, description="Datos completos de la sucursal")
    
    # Datos del sector (opcional)
    sector_data: Optional[SectorDataRequest] = Field(None, description="Datos completos del sector")
    
    # Datos del cliente (opcional)
    customer_data: Optional[CustomerDataRequest] = Field(None, description="Datos completos del cliente")
    
    # Información de la mercadería (opcional)
    unloading_time_minutes: Optional[int] = Field(None, gt=0, le=1440, description="Tiempo de descarga en minutos")
    reason: Optional[str] = Field(None, min_length=10, max_length=500, description="Motivo de la reserva")
    
    # Números de pedidos (opcional)
    order_numbers: Optional[List[OrderNumberRequest]] = Field(None, min_items=1, max_items=50, description="Lista de números de pedido")
    
    # Horario de la reserva (opcional)
    reservation_date: Optional[datetime] = Field(None, description="Fecha de la reserva")
    start_time: Optional[datetime] = Field(None, description="Hora de inicio de la reserva")
    end_time: Optional[datetime] = Field(None, description="Hora de fin de la reserva")
    
    # Información adicional (opcional)
    notes: Optional[str] = Field(None, max_length=1000, description="Notas adicionales")
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        """Validar que el horario de fin sea posterior al de inicio"""
        if v and 'start_time' in values and values['start_time'] and v <= values['start_time']:
            raise ValueError("El horario de fin debe ser posterior al de inicio")
        return v
    
    @validator('reservation_date')
    def validate_reservation_date(cls, v):
        """Validar que la fecha de reserva no sea en el pasado"""
        if v and v < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            raise ValueError("La fecha de reserva no puede ser en el pasado")
        return v
    
    def dict(self, *args, **kwargs):
        """Override dict method to convert datetime to ISO string"""
        data = super().dict(*args, **kwargs)
        if data.get('reservation_date'):
            data['reservation_date'] = data['reservation_date'].isoformat()
        if data.get('start_time'):
            data['start_time'] = data['start_time'].isoformat()
        if data.get('end_time'):
            data['end_time'] = data['end_time'].isoformat()
        return data 