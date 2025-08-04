"""
Request DTO para crear rampa en API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional


class CreateRampRequest(BaseModel):
    """Request para crear una rampa"""
    
    name: str = Field(..., min_length=1, max_length=100, description="Nombre de la rampa")
    branch_id: int = Field(..., gt=0, description="ID de la sucursal")
    is_available: bool = Field(True, description="Disponibilidad de la rampa")
    description: Optional[str] = Field(None, max_length=500, description="Descripción de la rampa")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Rampa Principal",
                "branch_id": 1,
                "is_available": True,
                "description": "Rampa principal de carga y descarga"
            }
        } 