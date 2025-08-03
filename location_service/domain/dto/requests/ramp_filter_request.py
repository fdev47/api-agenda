"""
DTO para request de filtro de rampas
"""
from pydantic import BaseModel, Field
from typing import Optional


class RampFilterRequest(BaseModel):
    """Request para filtrar rampas"""
    
    branch_id: Optional[int] = Field(None, gt=0, description="ID de la sucursal")
    name: Optional[str] = Field(None, description="Nombre de la rampa")
    is_available: Optional[bool] = Field(None, description="Disponibilidad de la rampa")
    skip: int = Field(0, ge=0, description="Número de registros a omitir")
    limit: int = Field(100, ge=1, le=1000, description="Número máximo de registros")
    sort_by: Optional[str] = Field(None, description="Campo para ordenar")
    sort_order: Optional[str] = Field(None, description="Orden (asc/desc)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "branch_id": 1,
                "name": "Rampa",
                "is_available": True,
                "skip": 0,
                "limit": 10,
                "sort_by": "name",
                "sort_order": "asc"
            }
        } 