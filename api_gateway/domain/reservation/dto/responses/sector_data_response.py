"""
DTO de response para datos de sector en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional


class SectorDataResponse(BaseModel):
    """DTO para datos de sector"""
    sector_id: int = Field(..., description="ID del sector")
    name: str = Field(..., description="Nombre del sector")
    description: Optional[str] = Field(None, description="Descripción del sector")
    sector_type_id: int = Field(..., description="ID del tipo de sector")
    sector_type_name: Optional[str] = Field(None, description="Nombre del tipo de sector")
    capacity: Optional[int] = Field(None, description="Capacidad del sector")
    measurement_unit_id: Optional[int] = Field(None, description="ID de la unidad de medida")
    measurement_unit_name: Optional[str] = Field(None, description="Nombre de la unidad de medida") 