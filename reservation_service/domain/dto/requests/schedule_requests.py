from datetime import date, time
from typing import Optional
from pydantic import BaseModel, Field, validator

from ...entities.day_of_week import DayOfWeek


class CreateBranchScheduleRequest(BaseModel):
    """Solicitud para crear un horario de sucursal"""
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    day_of_week: DayOfWeek = Field(..., description="Día de la semana")
    start_time: time = Field(..., description="Hora de inicio")
    end_time: time = Field(..., description="Hora de fin")
    interval_minutes: int = Field(60, gt=0, le=1440, description="Intervalo en minutos (por defecto 60)")
    is_active: bool = Field(True, description="Si el horario está activo")
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        """Validar que el tiempo de fin sea posterior al de inicio"""
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError("El tiempo de fin debe ser posterior al de inicio")
        return v
    
    @validator('interval_minutes')
    def validate_interval(cls, v, values):
        """Validar que el intervalo sea válido"""
        if 'start_time' in values and 'end_time' in values:
            start_minutes = values['start_time'].hour * 60 + values['start_time'].minute
            end_minutes = values['end_time'].hour * 60 + values['end_time'].minute
            duration = end_minutes - start_minutes
            
            if v > duration:
                raise ValueError("El intervalo no puede ser mayor que la duración total del horario")
        return v


class UpdateBranchScheduleRequest(BaseModel):
    """Solicitud para actualizar un horario de sucursal"""
    day_of_week: Optional[DayOfWeek] = Field(None, description="Día de la semana")
    start_time: Optional[time] = Field(None, description="Hora de inicio")
    end_time: Optional[time] = Field(None, description="Hora de fin")
    interval_minutes: Optional[int] = Field(None, gt=0, le=1440, description="Intervalo en minutos")
    is_active: Optional[bool] = Field(None, description="Si el horario está activo")
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        """Validar que el tiempo de fin sea posterior al de inicio"""
        if v and 'start_time' in values and values['start_time']:
            if v <= values['start_time']:
                raise ValueError("El tiempo de fin debe ser posterior al de inicio")
        return v


class GetAvailableSlotsRequest(BaseModel):
    """Solicitud para obtener slots disponibles"""
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    schedule_date: date = Field(..., description="Fecha para consultar disponibilidad")
    
    @validator('schedule_date')
    def validate_date_not_past(cls, v):
        """Validar que la fecha no sea en el pasado"""
        from datetime import date as today_date
        if v < today_date.today():
            raise ValueError("No se puede consultar disponibilidad para fechas pasadas")
        return v


class GetBranchSchedulesRequest(BaseModel):
    """Solicitud para obtener horarios de una sucursal"""
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    day_of_week: Optional[DayOfWeek] = Field(None, description="Filtrar por día específico")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo") 