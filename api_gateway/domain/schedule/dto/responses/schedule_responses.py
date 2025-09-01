"""
DTOs de respuestas para schedule en el API Gateway
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import time, date, datetime
from enum import Enum


class DayOfWeek(int, Enum):
    """Días de la semana"""
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class BranchScheduleResponse(BaseModel):
    """DTO para respuesta de horario de sucursal"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID del horario")
    branch_id: int = Field(..., description="ID de la sucursal")
    day_of_week: DayOfWeek = Field(..., description="Día de la semana")
    start_time: time = Field(..., description="Hora de inicio")
    end_time: time = Field(..., description="Hora de fin")
    is_active: bool = Field(..., description="Estado activo del horario")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")


class AvailableSlotResponse(BaseModel):
    """DTO para respuesta de slot disponible"""
    start_time: time = Field(..., description="Hora de inicio del slot")
    end_time: time = Field(..., description="Hora de fin del slot")
    is_available: bool = Field(..., description="Disponibilidad del slot")


class AvailableSlotsResponse(BaseModel):
    """DTO para respuesta de slots disponibles"""
    branch_id: int = Field(..., description="ID de la sucursal")
    schedule_date: date = Field(..., description="Fecha consultada")
    slots: List[AvailableSlotResponse] = Field(..., description="Lista de slots")
    total_slots: int = Field(..., description="Total de slots")
    available_slots: int = Field(..., description="Slots disponibles")


class BranchScheduleListResponse(BaseModel):
    """DTO para respuesta de lista de horarios de sucursal"""
    branch_id: int = Field(..., description="ID de la sucursal")
    schedules: List[BranchScheduleResponse] = Field(..., description="Lista de horarios")
    total: int = Field(..., description="Total de horarios")


class CreateBranchScheduleResponse(BaseModel):
    """DTO para respuesta de creación de horario"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de la operación")
    schedule_id: int = Field(..., description="ID del horario creado")


class UpdateBranchScheduleResponse(BaseModel):
    """DTO para respuesta de actualización de horario"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de la operación")
    requires_confirmation: bool = Field(default=False, description="Requiere confirmación")
    schedule: Optional[BranchScheduleResponse] = Field(None, description="Horario actualizado")
    impact_analysis: Optional[Dict[str, Any]] = Field(None, description="Análisis de impacto de los cambios")


class DeleteBranchScheduleResponse(BaseModel):
    """DTO para respuesta de eliminación de horario"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de la operación")
    schedule_id: int = Field(..., description="ID del horario eliminado") 