"""
Response DTO para rampa en API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RampResponse(BaseModel):
    """Response para una rampa"""
    
    id: int = Field(..., description="ID de la rampa")
    name: str = Field(..., description="Nombre de la rampa")
    branch_id: int = Field(..., description="ID de la sucursal")
    is_available: bool = Field(..., description="Disponibilidad de la rampa")
    description: Optional[str] = Field(None, description="Descripción de la rampa")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Rampa Principal",
                "branch_id": 1,
                "is_available": True,
                "description": "Rampa principal de carga y descarga",
                "created_at": "2025-08-03T22:00:00",
                "updated_at": "2025-08-03T22:00:00"
            }
        } 