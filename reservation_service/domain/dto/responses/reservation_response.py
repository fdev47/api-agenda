"""
Response DTO para reserva completa
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from .customer_data_response import CustomerDataResponse
from .main_reservation_response import MainReservationResponse


class ReservationResponse(BaseModel):
    """Response para una reserva completa"""
    
    # Identificación básica
    id: int = Field(..., description="ID de la reserva")
    user_id: int = Field(..., description="ID del usuario que hizo la reserva")
    customer_id: Optional[int] = Field(None, description="ID del cliente en el sistema")
    
    # ID de la sucursal (sin datos completos)
    branch_id: int = Field(..., description="ID de la sucursal")
    
    # Main reservations (sectores con rampa)
    main_reservations: List[MainReservationResponse] = Field(..., description="Lista de main_reservations creadas")
    
    # Datos del cliente (completos)
    customer_data: CustomerDataResponse = Field(..., description="Datos completos del cliente")
    
    # Información de la mercadería
    unloading_time_minutes: int = Field(..., description="Tiempo de descarga en minutos")
    unloading_time_hours: float = Field(..., description="Tiempo de descarga en horas")
    reason: str = Field(..., description="Motivo de la reserva")
    cargo_type: Optional[str] = Field(None, description="Tipo de carga")
    
    # Horario de la reserva
    reservation_date: datetime = Field(..., description="Fecha de la reserva")
    start_time: datetime = Field(..., description="Hora de inicio de la reserva")
    end_time: datetime = Field(..., description="Hora de fin de la reserva")
    
    # Estado y metadatos
    status: str = Field(..., description="Estado de la reserva")
    notes: Optional[str] = Field(None, description="Notas adicionales")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")
    
    # Métodos de conveniencia
    def is_active(self) -> bool:
        """Verifica si la reserva está activa"""
        return self.status in ["pending", "confirmed"]
    
    def is_cancelled(self) -> bool:
        """Verifica si la reserva está cancelada"""
        return self.status == "cancelled"
    
    def is_completed(self) -> bool:
        """Verifica si la reserva está completada"""
        return self.status == "completed"
    