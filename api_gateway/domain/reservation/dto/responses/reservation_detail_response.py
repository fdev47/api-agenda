"""
Response DTO para reserva con detalle completo en API Gateway
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

from .complete_reservation_response import CompleteReservationResponse
from .reject_reservation_response import RejectReservationResponse


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
    
    # Datos básicos de la reserva
    id: int = Field(..., description="ID de la reserva")
    user_id: Optional[int] = Field(None, description="ID del usuario")
    customer_id: Optional[int] = Field(None, description="ID del cliente")
    
    # Datos de la sucursal
    branch_data: Dict[str, Any] = Field(..., description="Datos completos de la sucursal")
    
    # Datos del sector
    sector_data: Dict[str, Any] = Field(..., description="Datos completos del sector")
    
    # Datos del cliente
    customer_data: Dict[str, Any] = Field(..., description="Datos completos del cliente")
    
    # Información de la mercadería
    merchandise_description: str = Field(..., description="Descripción de la mercadería")
    merchandise_quantity: int = Field(..., description="Cantidad de mercadería")
    merchandise_unit: str = Field(..., description="Unidad de medida")
    cargo_type: Optional[str] = Field(None, description="Tipo de carga")
    ramp_id: Optional[int] = Field(None, description="ID de la rampa asignada")
    
    # Horarios
    schedule_date: str = Field(..., description="Fecha de la reserva")
    schedule_start_time: str = Field(..., description="Hora de inicio")
    schedule_end_time: str = Field(..., description="Hora de fin")
    
    # Estado y metadatos
    status: ReservationStatus = Field(..., description="Estado de la reserva")
    special_requirements: Optional[str] = Field(None, description="Requerimientos especiales")
    order_numbers: list = Field(..., description="Lista de números de pedido")
    
    # Timestamps
    created_at: str = Field(..., description="Fecha de creación")
    updated_at: str = Field(..., description="Fecha de última actualización")
    
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
        if status == ReservationStatus.COMPLETED:
            return ClosingSummaryType.COMPLETED
        elif status == ReservationStatus.CANCELLED:
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
                    "address": "Av. Principal 123"
                },
                "sector_data": {
                    "sector_id": 1,
                    "name": "Sector A",
                    "sector_type_id": 1
                },
                "customer_data": {
                    "customer_id": 456,
                    "name": "Cliente Ejemplo",
                    "email": "cliente@ejemplo.com"
                },
                "merchandise_description": "Carga de productos",
                "merchandise_quantity": 120,
                "merchandise_unit": "minutos",
                "cargo_type": "PESADO",
                "schedule_date": "2025-08-03",
                "schedule_start_time": "10:00",
                "schedule_end_time": "12:00",
                "status": "COMPLETED",
                "special_requirements": "Manejo especial",
                "order_numbers": ["ORD-001", "ORD-002"],
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