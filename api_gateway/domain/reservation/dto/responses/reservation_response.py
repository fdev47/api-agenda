"""
Response DTO para reserva completa en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from .order_number_response import OrderNumberResponse
from .customer_data_response import CustomerDataResponse
from .branch_data_response import BranchDataResponse
from .sector_data_response import SectorDataResponse


class ReservationResponse(BaseModel):
    """Response para una reserva completa"""
    
    # Identificación básica
    id: int = Field(..., description="ID de la reserva")
    user_id: int = Field(..., description="ID del usuario que hizo la reserva")
    customer_id: Optional[int] = Field(None, description="ID del cliente en el sistema")
    
    # Datos de la sucursal (completos)
    branch_data: BranchDataResponse = Field(..., description="Datos completos de la sucursal")
    
    # Datos del sector (completos)
    sector_data: SectorDataResponse = Field(..., description="Datos completos del sector")
    
    # Datos del cliente (completos)
    customer_data: CustomerDataResponse = Field(..., description="Datos completos del cliente")
    
    # Información de la mercadería
    unloading_time_minutes: int = Field(..., description="Tiempo de descarga en minutos")
    unloading_time_hours: float = Field(..., description="Tiempo de descarga en horas")
    reason: str = Field(..., description="Motivo de la reserva")
    cargo_type: Optional[str] = Field(None, description="Tipo de carga")
    
    # Números de pedidos
    order_numbers: List[OrderNumberResponse] = Field(..., description="Lista de números de pedido")
    
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
    
    def get_order_codes(self) -> List[str]:
        """Obtiene la lista de códigos de pedidos"""
        return [order.code for order in self.order_numbers] 