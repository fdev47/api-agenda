"""
Request DTO para obtener reservas por período en el API Gateway
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ReservationPeriodRequest(BaseModel):
    """Request para obtener reservas en un período de tiempo"""
    
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    start_time: datetime = Field(..., description="Fecha y hora de inicio del período (YYYY-MM-DD HH:MM:SS)")
    end_time: datetime = Field(..., description="Fecha y hora de fin del período (YYYY-MM-DD HH:MM:SS)")
    status: Optional[str] = Field(None, description="Estado de la reserva (PENDING, CONFIRMED, COMPLETED, CANCELLED)")
    
    @field_validator("start_time", "end_time")
    @classmethod
    def validate_datetime(cls, v):
        """Validar que las fechas sean válidas"""
        if not isinstance(v, datetime):
            raise ValueError("Debe ser una fecha y hora válida")
        return v
    
    @field_validator("end_time")
    @classmethod
    def validate_end_after_start(cls, v, info):
        """Validar que la fecha de fin sea posterior a la de inicio"""
        start_time = info.data.get("start_time")
        if start_time and v <= start_time:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        return v
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        """Validar que el estado sea válido"""
        if v is not None:
            valid_statuses = ["PENDING", "CONFIRMED", "COMPLETED", "CANCELLED", "REJECTED", "RESCHEDULING_REQUIRED"]
            if v.upper() not in valid_statuses:
                raise ValueError(f"Estado inválido. Valores permitidos: {', '.join(valid_statuses)}")
            return v.upper()
        return v

