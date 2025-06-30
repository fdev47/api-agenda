from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class OrderNumberRequest(BaseModel):
    """Request para un número de pedido"""
    code: str = Field(..., min_length=1, max_length=50, description="Código del pedido")
    description: Optional[str] = Field(None, max_length=200, description="Descripción opcional del pedido")


class CustomerDataRequest(BaseModel):
    """Request para datos del cliente"""
    # ID de referencia (opcional, puede no existir en el sistema)
    customer_id: Optional[int] = Field(None, gt=0, description="ID del cliente en el sistema")
    # Datos completos al momento de la reserva
    ruc: str = Field(..., min_length=10, max_length=20, description="RUC del cliente")
    company_name: str = Field(..., min_length=2, max_length=100, description="Nombre de la empresa")
    phone_number: str = Field(..., min_length=7, max_length=20, description="Número de teléfono")


class BranchDataRequest(BaseModel):
    """Request para datos de la sucursal"""
    # ID de referencia en location_service
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    # Datos completos al momento de la reserva
    name: str = Field(..., min_length=2, max_length=100, description="Nombre de la sucursal")
    code: str = Field(..., min_length=1, max_length=20, description="Código de la sucursal")
    address: str = Field(..., min_length=10, max_length=200, description="Dirección de la sucursal")
    country_id: int = Field(..., gt=0, description="ID del país")
    country_name: str = Field(..., min_length=2, max_length=50, description="Nombre del país")
    state_id: int = Field(..., gt=0, description="ID del estado")
    state_name: str = Field(..., min_length=2, max_length=50, description="Nombre del estado")
    city_id: int = Field(..., gt=0, description="ID de la ciudad")
    city_name: str = Field(..., min_length=2, max_length=50, description="Nombre de la ciudad")


class SectorDataRequest(BaseModel):
    """Request para datos del sector"""
    # ID de referencia en location_service
    sector_id: int = Field(..., gt=0, description="ID del sector")
    # Datos completos al momento de la reserva
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del sector")
    description: Optional[str] = Field(None, max_length=200, description="Descripción del sector")
    sector_type_id: int = Field(..., gt=0, description="ID del tipo de sector")
    sector_type_name: str = Field(..., min_length=2, max_length=50, description="Nombre del tipo de sector")
    measurement_unit: str = Field(..., min_length=1, max_length=20, description="Unidad de medida")


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


class ReservationFilterRequest(BaseModel):
    """Request para filtrar reservas"""
    
    # Filtros por usuario/cliente
    user_id: Optional[int] = None
    customer_id: Optional[int] = None
    
    # Filtros por sucursal
    branch_id: Optional[int] = None
    branch_name: Optional[str] = None
    
    # Filtros por sector
    sector_id: Optional[int] = None
    sector_name: Optional[str] = None
    
    # Filtros por cliente
    customer_ruc: Optional[str] = None
    company_name: Optional[str] = None
    
    # Filtros por fecha
    reservation_date_from: Optional[datetime] = None
    reservation_date_to: Optional[datetime] = None
    
    # Filtros por estado
    status: Optional[str] = None
    
    # Filtros por pedido
    order_code: Optional[str] = None
    
    # Paginación
    page: int = Field(1, ge=1, description="Número de página")
    limit: int = Field(10, ge=1, le=100, description="Elementos por página")
    
    @property
    def offset(self) -> int:
        """Calcular el offset para la paginación"""
        return (self.page - 1) * self.limit 