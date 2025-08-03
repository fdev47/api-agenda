"""
DTO para respuesta de rampa disponible
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AvailableRampResponse(BaseModel):
    """Response para rampa disponible"""
    
    ramp_id: int = Field(..., description="ID de la rampa")
    ramp_name: str = Field(..., description="Nombre de la rampa")
    branch_id: int = Field(..., description="ID de la sucursal")
    is_available: bool = Field(..., description="Indica si la rampa está disponible")
    start_date: datetime = Field(..., description="Fecha y hora de inicio")
    end_date: datetime = Field(..., description="Fecha y hora de fin")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ramp_id": 1,
                "ramp_name": "Rampa 1",
                "branch_id": 1,
                "is_available": True,
                "start_date": "2025-12-08T10:00:00",
                "end_date": "2025-12-08T11:30:00"
            }
        } 