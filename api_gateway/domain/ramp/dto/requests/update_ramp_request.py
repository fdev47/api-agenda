"""
Request DTO para actualizar rampa en API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional


class UpdateRampRequest(BaseModel):
    """Request para actualizar una rampa"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre de la rampa")
    branch_id: Optional[int] = Field(None, gt=0, description="ID de la sucursal")
    is_available: Optional[bool] = Field(None, description="Disponibilidad de la rampa")
    description: Optional[str] = Field(None, max_length=500, description="Descripción de la rampa")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Rampa Principal Actualizada",
                "is_available": False,
                "description": "Rampa en mantenimiento"
            }
        } 