"""
Response DTO para slots disponibles de rampas
"""
from pydantic import BaseModel, Field
from datetime import date, time
from typing import List


class SlotInfo(BaseModel):
    """Información de un slot de tiempo"""
    
    start_time: time = Field(..., description="Hora de inicio del slot")
    end_time: time = Field(..., description="Hora de fin del slot")
    is_available: bool = Field(..., description="Indica si el slot está disponible")
    ramp_id: int = Field(..., description="ID de la rampa asignada al slot")
    ramp_name: str = Field(..., description="Nombre de la rampa asignada al slot")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "start_time": "08:00:00",
                "end_time": "10:00:00",
                "is_available": True,
                "ramp_id": 1,
                "ramp_name": "Rampa 1"
            }
        }
    }


class RampSlotsResponse(BaseModel):
    """Response con los slots disponibles de rampas"""
    
    schedule_date: date = Field(..., description="Fecha consultada")
    slots: List[SlotInfo] = Field(..., description="Lista de slots de tiempo")
    total_slots: int = Field(..., description="Total de slots")
    available_slots: int = Field(..., description="Slots disponibles")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "schedule_date": "2025-11-10",
                "slots": [
                    {
                        "start_time": "08:00:00",
                        "end_time": "10:00:00",
                        "is_available": True,
                        "ramp_id": 1,
                        "ramp_name": "Rampa 1"
                    },
                    {
                        "start_time": "10:00:00",
                        "end_time": "12:00:00",
                        "is_available": False,
                        "ramp_id": 1,
                        "ramp_name": "Rampa 1"
                    }
                ],
                "total_slots": 2,
                "available_slots": 1
            }
        }
    }

