"""
DTO para respuesta de rampa
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RampResponse(BaseModel):
    """Response para una rampa"""
    
    id: int = Field(..., description="ID de la rampa")
    name: str = Field(..., description="Nombre de la rampa")
    is_available: bool = Field(..., description="Indica si la rampa está disponible")
    branch_id: int = Field(..., description="ID de la sucursal")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Rampa 1",
                "is_available": True,
                "branch_id": 1,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        } 