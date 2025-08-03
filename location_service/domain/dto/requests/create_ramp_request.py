"""
DTO para request de crear rampa
"""
from pydantic import BaseModel, Field
from typing import Optional


class CreateRampRequest(BaseModel):
    """Request para crear una rampa"""
    
    name: str = Field(..., min_length=1, max_length=100, description="Nombre de la rampa")
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    is_available: bool = Field(True, description="Indica si la rampa está disponible")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Rampa 1",
                "branch_id": 1,
                "is_available": True
            }
        } 