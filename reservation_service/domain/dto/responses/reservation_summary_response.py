"""
Response DTO para resumen de reserva
"""
from pydantic import BaseModel, Field
from datetime import datetime


class ReservationSummaryResponse(BaseModel):
    """Response resumido para una reserva (sin datos completos)"""
    id: int = Field(..., description="ID de la reserva")
    customer_name: str = Field(..., description="Nombre del cliente")
    customer_email: str = Field(..., description="Email del cliente")
    branch_id: int = Field(..., description="ID de la sucursal")
    branch_name: str = Field(..., description="Nombre de la sucursal")
    sector_id: int = Field(..., description="ID del sector")
    sector_name: str = Field(..., description="Nombre del sector")
    reservation_date: datetime = Field(..., description="Fecha de la reserva")
    start_time: datetime = Field(..., description="Hora de inicio")
    end_time: datetime = Field(..., description="Hora de fin")
    status: str = Field(..., description="Estado de la reserva")
    order_count: int = Field(..., description="Cantidad de pedidos")
    unloading_time_hours: float = Field(..., description="Tiempo de descarga en horas") 