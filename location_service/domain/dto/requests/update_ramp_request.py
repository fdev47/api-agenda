"""
DTO para request de actualizar rampa
"""
from pydantic import BaseModel, Field
from typing import Optional


class UpdateRampRequest(BaseModel):
    """Request para actualizar una rampa"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre de la rampa")
    is_available: Optional[bool] = Field(None, description="Indica si la rampa está disponible")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Rampa 1 Actualizada",
                "is_available": True
            }
        } 