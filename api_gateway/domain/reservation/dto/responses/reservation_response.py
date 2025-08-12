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
    id: Optional[int] = Field(None, description="ID de la reserva")
    user_id: Optional[int] = Field(None, description="ID del usuario que hizo la reserva")
    customer_id: Optional[int] = Field(None, description="ID del cliente en el sistema")
    
    # Datos de la sucursal (completos)
    branch_data: Optional[BranchDataResponse] = Field(None, description="Datos completos de la sucursal")
    
    # Datos del sector (completos)
    sector_data: Optional[SectorDataResponse] = Field(None, description="Datos completos del sector")
    
    # Datos del cliente (completos)
    customer_data: Optional[CustomerDataResponse] = Field(None, description="Datos completos del cliente")
    
    # Información de la mercadería
    unloading_time_minutes: Optional[int] = Field(None, description="Tiempo de descarga en minutos")
    unloading_time_hours: Optional[float] = Field(None, description="Tiempo de descarga en horas")
    reason: Optional[str] = Field(None, description="Motivo de la reserva")
    cargo_type: Optional[str] = Field(None, description="Tipo de carga")
    ramp_id: Optional[int] = Field(None, description="ID de la rampa asignada")
    
    # Números de pedidos
    order_numbers: Optional[List[OrderNumberResponse]] = Field(None, description="Lista de números de pedido")
    
    # Horario de la reserva
    reservation_date: Optional[datetime] = Field(None, description="Fecha de la reserva")
    start_time: Optional[datetime] = Field(None, description="Hora de inicio de la reserva")
    end_time: Optional[datetime] = Field(None, description="Hora de fin de la reserva")
    
    # Estado y metadatos
    status: Optional[str] = Field(None, description="Estado de la reserva")
    notes: Optional[str] = Field(None, description="Notas adicionales")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")
    
    # Métodos de conveniencia
    def is_active(self) -> bool:
        """Verifica si la reserva está activa"""
        return self.status in ["pending", "confirmed"] if self.status else False
    
    def is_cancelled(self) -> bool:
        """Verifica si la reserva está cancelada"""
        return self.status == "cancelled" if self.status else False
    
    def is_completed(self) -> bool:
        """Verifica si la reserva está completada"""
        return self.status == "completed" if self.status else False
    
    def get_order_codes(self) -> List[str]:
        """Obtiene la lista de códigos de pedidos"""
        if self.order_numbers:
            return [order.code for order in self.order_numbers if order and order.code]
        return [] 