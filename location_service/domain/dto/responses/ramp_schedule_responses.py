"""
DTOs de responses para horarios de rampas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, time


class RampScheduleResponse(BaseModel):
    """DTO para respuesta de horario de rampa"""
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "ramp_id": 1,
                "day_of_week": 1,
                "day_name": "Lunes",
                "name": "Turno 1",
                "start_time": "07:00:00",
                "end_time": "12:00:00",
                "is_active": True,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": None
            }
        }
    )
    
    id: int = Field(..., description="ID del horario")
    ramp_id: int = Field(..., description="ID de la rampa")
    day_of_week: int = Field(..., description="Día de la semana (1=Lunes, 7=Domingo)")
    day_name: str = Field(..., description="Nombre del día")
    name: str = Field(..., description="Nombre del horario")
    start_time: time = Field(..., description="Hora de inicio")
    end_time: time = Field(..., description="Hora de fin")
    is_active: bool = Field(..., description="Estado activo del horario")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")


class RampScheduleListResponse(BaseModel):
    """DTO para lista de horarios de rampas"""
    schedules: List[RampScheduleResponse] = Field(..., description="Lista de horarios")
    total: int = Field(..., description="Total de horarios")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de la página")


class RampScheduleCreatedResponse(BaseModel):
    """DTO para respuesta de horario creado"""
    id: int = Field(..., description="ID del horario creado")
    ramp_id: int = Field(..., description="ID de la rampa")
    day_of_week: int = Field(..., description="Día de la semana")
    day_name: str = Field(..., description="Nombre del día")
    name: str = Field(..., description="Nombre del horario")
    start_time: time = Field(..., description="Hora de inicio")
    end_time: time = Field(..., description="Hora de fin")
    is_active: bool = Field(..., description="Estado activo")
    message: str = Field(default="Horario creado exitosamente", description="Mensaje de confirmación")


class RampScheduleUpdatedResponse(BaseModel):
    """DTO para respuesta de horario actualizado"""
    id: int = Field(..., description="ID del horario")
    ramp_id: int = Field(..., description="ID de la rampa")
    day_of_week: int = Field(..., description="Día de la semana")
    day_name: str = Field(..., description="Nombre del día")
    name: str = Field(..., description="Nombre del horario")
    start_time: time = Field(..., description="Hora de inicio")
    end_time: time = Field(..., description="Hora de fin")
    is_active: bool = Field(..., description="Estado activo")
    message: str = Field(default="Horario actualizado exitosamente", description="Mensaje de confirmación")


class RampScheduleDeletedResponse(BaseModel):
    """DTO para respuesta de horario eliminado"""
    id: int = Field(..., description="ID del horario eliminado")
    message: str = Field(default="Horario eliminado exitosamente", description="Mensaje de confirmación")

