"""
DTOs de requests para horarios de rampas en el API Gateway
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import time


class CreateRampScheduleRequest(BaseModel):
    """DTO para crear un horario de rampa"""
    ramp_id: int = Field(..., gt=0, description="ID de la rampa")
    day_of_week: int = Field(..., ge=1, le=7, description="Día de la semana (1=Lunes, 7=Domingo)")
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del horario")
    start_time: time = Field(..., description="Hora de inicio (formato HH:MM:SS)")
    end_time: time = Field(..., description="Hora de fin (formato HH:MM:SS)")
    is_active: bool = Field(True, description="Estado activo del horario")
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre del horario no puede estar vacío')
        return v.strip()
    
    @validator('end_time')
    def validate_time_range(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('La hora de fin debe ser mayor a la hora de inicio')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "ramp_id": 1,
                "day_of_week": 1,
                "name": "Turno 1",
                "start_time": "07:00:00",
                "end_time": "12:00:00",
                "is_active": True
            }
        }


class UpdateRampScheduleRequest(BaseModel):
    """DTO para actualizar un horario de rampa"""
    day_of_week: Optional[int] = Field(None, ge=1, le=7, description="Día de la semana (1=Lunes, 7=Domingo)")
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del horario")
    start_time: Optional[time] = Field(None, description="Hora de inicio")
    end_time: Optional[time] = Field(None, description="Hora de fin")
    is_active: Optional[bool] = Field(None, description="Estado activo del horario")
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('El nombre del horario no puede estar vacío')
            return v.strip()
        return v
    
    @validator('end_time')
    def validate_time_range(cls, v, values):
        if v is not None and 'start_time' in values and values['start_time'] is not None:
            if v <= values['start_time']:
                raise ValueError('La hora de fin debe ser mayor a la hora de inicio')
        return v


class RampScheduleFilterRequest(BaseModel):
    """DTO para filtrar horarios de rampas"""
    ramp_id: Optional[int] = Field(None, gt=0, description="Filtrar por rampa")
    day_of_week: Optional[int] = Field(None, ge=1, le=7, description="Filtrar por día de la semana")
    name: Optional[str] = Field(None, description="Filtrar por nombre del horario")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    limit: int = Field(100, ge=1, le=1000, description="Límite de resultados")
    offset: int = Field(0, ge=0, description="Offset para paginación")

