from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class OrderNumberResponse(BaseModel):
    """Response para un número de pedido"""
    code: str = Field(..., description="Código del pedido")
    description: Optional[str] = Field(None, description="Descripción del pedido")


class CustomerDataResponse(BaseModel):
    """Response para datos del cliente"""
    # ID de referencia (opcional, puede no existir en el sistema)
    customer_id: Optional[int] = Field(None, description="ID del cliente en el sistema")
    # Datos completos al momento de la reserva
    ruc: str = Field(..., description="RUC del cliente")
    company_name: str = Field(..., description="Nombre de la empresa")
    phone_number: str = Field(..., description="Número de teléfono")


class BranchDataResponse(BaseModel):
    """Response para datos de la sucursal"""
    # ID de referencia en location_service
    branch_id: int = Field(..., description="ID de la sucursal")
    # Datos completos al momento de la reserva
    name: str = Field(..., description="Nombre de la sucursal")
    code: str = Field(..., description="Código de la sucursal")
    address: str = Field(..., description="Dirección de la sucursal")
    country_id: int = Field(..., description="ID del país")
    country_name: str = Field(..., description="Nombre del país")
    state_id: int = Field(..., description="ID del estado")
    state_name: str = Field(..., description="Nombre del estado")
    city_id: int = Field(..., description="ID de la ciudad")
    city_name: str = Field(..., description="Nombre de la ciudad")


class SectorDataResponse(BaseModel):
    """Response para datos del sector"""
    # ID de referencia en location_service
    sector_id: int = Field(..., description="ID del sector")
    # Datos completos al momento de la reserva
    name: str = Field(..., description="Nombre del sector")
    description: Optional[str] = Field(None, description="Descripción del sector")
    sector_type_id: int = Field(..., description="ID del tipo de sector")
    sector_type_name: str = Field(..., description="Nombre del tipo de sector")
    measurement_unit: str = Field(..., description="Unidad de medida")


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


class ReservationListResponse(BaseModel):
    """Response para lista de reservas con paginación"""
    items: List[ReservationResponse] = Field(..., description="Lista de reservas")
    total: int = Field(..., description="Total de reservas")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de la página")
    pages: int = Field(..., description="Total de páginas")


class ReservationSummaryResponse(BaseModel):
    """Response resumido para una reserva (sin datos completos)"""
    id: int = Field(..., description="ID de la reserva")
    customer_company_name: str = Field(..., description="Nombre de la empresa del cliente")
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


class ReservationSummaryListResponse(BaseModel):
    """Response para lista resumida de reservas"""
    items: List[ReservationSummaryResponse] = Field(..., description="Lista de reservas resumidas")
    total: int = Field(..., description="Total de reservas")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de la página")
    pages: int = Field(..., description="Total de páginas") 