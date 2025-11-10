"""
Request DTO para obtener slots disponibles de rampas
"""
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional


class RampSlotsRequest(BaseModel):
    """Request para obtener slots disponibles de rampas"""
    
    type: str = Field(..., description="Tipo de carga (SECO, FRIO, FLV)")
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    schedule_date: date = Field(..., description="Fecha para la cual se consultan los slots (YYYY-MM-DD)")
    interval_time: int = Field(..., gt=0, description="Intervalo de tiempo en minutos para cada slot")
    
    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validar que el tipo de carga sea válido"""
        valid_types = ["SECO", "FRIO", "FLV"]
        if v.upper() not in valid_types:
            raise ValueError(f"Tipo de carga debe ser uno de: {', '.join(valid_types)}")
        return v.upper()
    
    @field_validator("schedule_date")
    @classmethod
    def validate_schedule_date(cls, v: date) -> date:
        """Validar que la fecha no sea en el pasado"""
        from datetime import date as dt_date
        if v < dt_date.today():
            raise ValueError("La fecha no puede ser en el pasado")
        return v
    
    @field_validator("interval_time")
    @classmethod
    def validate_interval_time(cls, v: int) -> int:
        """Validar que el intervalo de tiempo sea razonable"""
        if v < 15:
            raise ValueError("El intervalo de tiempo debe ser al menos 15 minutos")
        if v > 480:
            raise ValueError("El intervalo de tiempo no puede ser mayor a 480 minutos (8 horas)")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "type": "SECO",
                "branch_id": 1,
                "schedule_date": "2025-11-10",
                "interval_time": 60
            }
        }
    }

