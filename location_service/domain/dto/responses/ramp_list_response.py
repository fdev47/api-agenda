"""
DTO para respuesta de lista de rampas
"""
from pydantic import BaseModel, Field
from typing import List
from .ramp_response import RampResponse


class RampListResponse(BaseModel):
    """Response para lista de rampas"""
    
    ramps: List[RampResponse] = Field(..., description="Lista de rampas")
    total: int = Field(..., description="Total de rampas")
    skip: int = Field(..., description="Número de registros omitidos")
    limit: int = Field(..., description="Número máximo de registros")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ramps": [
                    {
                        "id": 1,
                        "name": "Rampa 1",
                        "is_available": True,
                        "branch_id": 1,
                        "created_at": "2025-01-01T00:00:00",
                        "updated_at": "2025-01-01T00:00:00"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 10
            }
        } 