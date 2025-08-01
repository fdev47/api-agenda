"""
DTO de response para resumen de reserva en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from .order_number_response import OrderNumberResponse


class ReservationSummaryResponse(BaseModel):
    """DTO para resumen de reserva"""
    id: int = Field(..., description="ID de la reserva")
    user_id: int = Field(..., description="ID del usuario")
    customer_name: str = Field(..., description="Nombre del cliente")
    branch_name: str = Field(..., description="Nombre de la sucursal")
    sector_name: str = Field(..., description="Nombre del sector")
    reservation_date: datetime = Field(..., description="Fecha de la reserva")
    start_time: datetime = Field(..., description="Hora de inicio")
    end_time: datetime = Field(..., description="Hora de fin")
    status: str = Field(..., description="Estado de la reserva")
    order_count: int = Field(..., description="Número de pedidos")
    order_codes: List[str] = Field(..., description="Códigos de pedidos")
    reason: str = Field(..., description="Motivo de la reserva")
    cargo_type: Optional[str] = Field(None, description="Tipo de carga")
    created_at: datetime = Field(..., description="Fecha de creación") 