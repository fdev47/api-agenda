"""
DTOs de requests para schedule en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import time, date
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


class CreateBranchScheduleRequest(BaseModel):
    """DTO para crear un horario de sucursal"""
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    day_of_week: DayOfWeek = Field(..., description="Día de la semana")
    start_time: time = Field(..., description="Hora de inicio")
    end_time: time = Field(..., description="Hora de fin")
    is_active: bool = Field(default=True, description="Estado activo del horario")


class UpdateBranchScheduleRequest(BaseModel):
    """DTO para actualizar un horario de sucursal"""
    day_of_week: Optional[DayOfWeek] = Field(None, description="Día de la semana")
    start_time: Optional[time] = Field(None, description="Hora de inicio")
    end_time: Optional[time] = Field(None, description="Hora de fin")
    is_active: Optional[bool] = Field(None, description="Estado activo del horario")


class GetAvailableSlotsRequest(BaseModel):
    """DTO para obtener slots disponibles"""
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    schedule_date: date = Field(..., description="Fecha para consultar disponibilidad")


class GetBranchSchedulesRequest(BaseModel):
    """DTO para obtener horarios de una sucursal"""
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    day_of_week: Optional[DayOfWeek] = Field(None, description="Día de la semana")
    is_active: Optional[bool] = Field(None, description="Estado activo del horario") 