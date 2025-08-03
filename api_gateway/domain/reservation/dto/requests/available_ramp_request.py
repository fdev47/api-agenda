"""
DTO para request de rampa disponible
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AvailableRampRequest(BaseModel):
    """Request para obtener una rampa disponible"""
    
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    start_date: str = Field(..., description="Fecha y hora de inicio (YYYY-MM-DD HH:MM:SS)")
    end_date: str = Field(..., description="Fecha y hora de fin (YYYY-MM-DD HH:MM:SS)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "branch_id": 1,
                "start_date": "2025-12-08 10:00:00",
                "end_date": "2025-12-08 11:30:00"
            }
        } 