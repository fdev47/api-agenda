"""
DTO de request para datos de sector en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class SectorDataRequest(BaseModel):
    """DTO para datos de sector"""
    # ID de referencia en location_service
    sector_id: int = Field(..., gt=0, description="ID del sector")
    # Datos completos al momento de la reserva
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del sector")
    description: Optional[str] = Field(None, max_length=200, description="Descripción del sector")
    sector_type_id: int = Field(..., gt=0, description="ID del tipo de sector")
    sector_type_name: str = Field(..., min_length=2, max_length=50, description="Nombre del tipo de sector")
    capacity: Optional[float] = Field(None, gt=0, description="Capacidad del sector")
    measurement_unit_id: int = Field(..., gt=0, description="ID de la unidad de medida")
    measurement_unit_name: str = Field(..., min_length=1, max_length=20, description="Nombre de la unidad de medida")
    
    # Nuevos campos para cantidades (opcionales)
    pallet_count: Optional[int] = Field(0, description="Cantidad de palets")
    granel_count: Optional[int] = Field(0, description="Cantidad de graneles")
    boxes_count: Optional[int] = Field(0, description="Cantidad de cajas")
    
    # Números de pedido asociados
    order_numbers: Optional[List[str]] = Field(None, description="Lista de números de pedido") 