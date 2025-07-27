from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel, Field

from ...entities.day_of_week import DayOfWeek
from ...entities.time_slot import TimeSlot


class TimeSlotResponse(BaseModel):
    """Respuesta para un slot de tiempo"""
    start_time: time = Field(..., description="Hora de inicio")
    end_time: time = Field(..., description="Hora de fin")
    is_available: bool = Field(..., description="Si el slot está disponible")
    reservation_id: Optional[int] = Field(None, description="ID de la reserva si está ocupado")
    duration_minutes: int = Field(..., description="Duración en minutos")
    duration_hours: float = Field(..., description="Duración en horas")
    
    class Config:
        json_encoders = {
            time: lambda v: v.strftime("%H:%M")
        }


class BranchScheduleResponse(BaseModel):
    """Respuesta para un horario de sucursal"""
    id: int = Field(..., description="ID del horario")
    branch_id: int = Field(..., description="ID de la sucursal")
    day_of_week: DayOfWeek = Field(..., description="Día de la semana")
    day_name: str = Field(..., description="Nombre del día")
    start_time: time = Field(..., description="Hora de inicio")
    end_time: time = Field(..., description="Hora de fin")
    interval_minutes: int = Field(..., description="Intervalo en minutos")
    is_active: bool = Field(..., description="Si el horario está activo")
    duration_minutes: int = Field(..., description="Duración total en minutos")
    duration_hours: float = Field(..., description="Duración total en horas")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de actualización")
    
    class Config:
        json_encoders = {
            time: lambda v: v.strftime("%H:%M")
        }


class AvailableSlotsResponse(BaseModel):
    """Respuesta con slots disponibles para una fecha"""
    branch_id: int = Field(..., description="ID de la sucursal")
    branch_name: str = Field(..., description="Nombre de la sucursal")
    date: datetime = Field(..., description="Fecha consultada")
    day_of_week: int = Field(..., description="Día de la semana (1-7)")
    day_name: str = Field(..., description="Nombre del día")
    slots: List[TimeSlotResponse] = Field(..., description="Lista de slots disponibles")
    total_slots: int = Field(..., description="Total de slots")
    available_slots: int = Field(..., description="Slots disponibles")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class BranchScheduleListResponse(BaseModel):
    """Respuesta con lista de horarios de sucursal"""
    schedules: List[BranchScheduleResponse] = Field(..., description="Lista de horarios")
    total: int = Field(..., description="Total de horarios")
    branch_id: int = Field(..., description="ID de la sucursal")


class CreateBranchScheduleResponse(BaseModel):
    """Respuesta para creación de horario"""
    id: int = Field(..., description="ID del horario creado")
    message: str = Field("Horario creado exitosamente", description="Mensaje de confirmación")


class UpdateBranchScheduleResponse(BaseModel):
    """Respuesta para actualización de horario"""
    id: int = Field(..., description="ID del horario actualizado")
    message: str = Field("Horario actualizado exitosamente", description="Mensaje de confirmación")


class DeleteBranchScheduleResponse(BaseModel):
    """Respuesta para eliminación de horario"""
    id: int = Field(..., description="ID del horario eliminado")
    message: str = Field("Horario eliminado exitosamente", description="Mensaje de confirmación") 