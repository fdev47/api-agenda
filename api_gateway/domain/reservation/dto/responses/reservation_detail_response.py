"""
Response DTO para reserva con detalle completo en API Gateway
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

from .complete_reservation_response import CompleteReservationResponse
from .reject_reservation_response import RejectReservationResponse
from .order_number_response import OrderNumberResponse
from .customer_data_response import CustomerDataResponse
from .branch_data_response import BranchDataResponse
from .sector_data_response import SectorDataResponse


class ReservationStatus(str, Enum):
    """Estados de reserva"""
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    RESCHEDULING_REQUIRED = "RESCHEDULING_REQUIRED"


class ClosingSummaryType(str, Enum):
    """Tipos de closing_summary"""
    COMPLETED = "completed"
    REJECTED = "rejected"
    NONE = "none"


class ReservationDetailResponse(BaseModel):
    """Response detallado para una reserva con closing_summary tipado"""
    
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
    ramp_id: Optional[int] = Field(None, description="ID de la rampa asignada")
    
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
    
    # Closing summary tipado
    closing_summary_type: ClosingSummaryType = Field(..., description="Tipo de closing_summary")
    closing_summary_completed: Optional[CompleteReservationResponse] = Field(None, description="Datos de completado")
    closing_summary_rejected: Optional[RejectReservationResponse] = Field(None, description="Datos de rechazo")
    
    @field_validator('closing_summary_type', mode='before')
    @classmethod
    def determine_closing_summary_type(cls, v, info):
        """Determinar el tipo de closing_summary basado en el status"""
        data = info.data
        status = data.get('status')
        if status == "COMPLETED":
            return ClosingSummaryType.COMPLETED
        elif status == "CANCELLED":
            return ClosingSummaryType.REJECTED
        else:
            return ClosingSummaryType.NONE
    
    @field_validator('closing_summary_completed', 'closing_summary_rejected', mode='before')
    @classmethod
    def validate_closing_summary(cls, v, info):
        """Validar que el closing_summary corresponda al tipo correcto"""
        data = info.data
        field_name = info.field_name
        closing_summary_type = data.get('closing_summary_type')
        closing_summary_raw = data.get('closing_summary')
        
        if not closing_summary_raw:
            return None
            
        if field_name == 'closing_summary_completed' and closing_summary_type == ClosingSummaryType.COMPLETED:
            return CompleteReservationResponse(**closing_summary_raw)
        elif field_name == 'closing_summary_rejected' and closing_summary_type == ClosingSummaryType.REJECTED:
            return RejectReservationResponse(**closing_summary_raw)
        
        return None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "customer_id": 456,
                "branch_data": {
                    "branch_id": 1,
                    "name": "Sucursal Principal",
                    "code": "SP001",
                    "address": "Av. Principal 123",
                    "country_id": 1,
                    "country_name": "Paraguay",
                    "state_id": 1,
                    "state_name": "Asunción",
                    "city_id": 1,
                    "city_name": "Asunción",
                    "ramp_id": 1,
                    "ramp_name": "Rampa 1"
                },
                "sector_data": {
                    "sector_id": 1,
                    "name": "Sector A",
                    "description": "Sector de descarga",
                    "sector_type_id": 1,
                    "sector_type_name": "Descarga",
                    "capacity": 100.0,
                    "measurement_unit_id": 1,
                    "measurement_unit_name": "minutos"
                },
                "customer_data": {
                    "customer_id": 456,
                    "auth_uid": "firebase_uid_123",
                    "ruc": "12345678-9",
                    "company_name": "Cliente Ejemplo",
                    "email": "cliente@ejemplo.com",
                    "username": "cliente_ejemplo",
                    "phone": "021-123456",
                    "cellphone_number": "0981234567",
                    "cellphone_country_code": "+595",
                    "address_id": "uuid-address-123",
                    "is_active": True
                },
                "unloading_time_minutes": 120,
                "unloading_time_hours": 2.0,
                "reason": "Descarga de productos",
                "cargo_type": "PESADO",
                "ramp_id": 1,
                "order_numbers": [
                    {
                        "id": 1,
                        "code": "ORD-001",
                        "reservation_id": 1
                    },
                    {
                        "id": 2,
                        "code": "ORD-002",
                        "reservation_id": 1
                    }
                ],
                "reservation_date": "2025-08-03T00:00:00",
                "start_time": "2025-08-03T10:00:00",
                "end_time": "2025-08-03T12:00:00",
                "status": "COMPLETED",
                "notes": "Manejo especial requerido",
                "created_at": "2025-08-03T10:00:00",
                "updated_at": "2025-08-03T12:00:00",
                "closing_summary_type": "completed",
                "closing_summary_completed": {
                    "user_id": "12345",
                    "user_name": "Juan Pérez",
                    "date": "2025-08-03T12:00:00",
                    "download_time": "2 horas",
                    "success_code": "SUCCESS_001",
                    "comment": "Descarga completada"
                },
                "closing_summary_rejected": None
            }
        }
    
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