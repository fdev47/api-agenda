"""
Response DTO para lista de rampas en API Gateway
"""
from pydantic import BaseModel, Field
from typing import List
from .ramp_response import RampResponse


class RampListResponse(BaseModel):
    """Response para lista de rampas"""
    
    ramps: List[RampResponse] = Field(..., description="Lista de rampas")
    total: int = Field(..., description="Total de registros")
    skip: int = Field(..., description="Número de registros omitidos")
    limit: int = Field(..., description="Número máximo de registros")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ramps": [
                    {
                        "id": 1,
                        "name": "Rampa Principal",
                        "branch_id": 1,
                        "is_available": True,
                        "description": "Rampa principal de carga y descarga",
                        "created_at": "2025-08-03T22:00:00",
                        "updated_at": "2025-08-03T22:00:00"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 10
            }
        } 