"""
DTO de response para datos de sector en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class SectorDataResponse(BaseModel):
    """DTO para datos de sector"""
    sector_id: Optional[int] = Field(None, description="ID del sector")
    name: Optional[str] = Field(None, description="Nombre del sector")
    description: Optional[str] = Field(None, description="Descripción del sector")
    sector_type_id: Optional[int] = Field(None, description="ID del tipo de sector")
    sector_type_name: Optional[str] = Field(None, description="Nombre del tipo de sector")
    capacity: Optional[int] = Field(None, description="Capacidad del sector")
    measurement_unit_id: Optional[int] = Field(None, description="ID de la unidad de medida")
    measurement_unit_name: Optional[str] = Field(None, description="Nombre de la unidad de medida")
    
    # Nuevos campos para cantidades (opcionales para compatibilidad con reservas existentes)
    pallet_count: Optional[int] = Field(0, description="Cantidad de palets")
    granel_count: Optional[int] = Field(0, description="Cantidad de graneles")
    boxes_count: Optional[int] = Field(0, description="Cantidad de cajas")
    
    # Números de pedido asociados
    order_numbers: Optional[List[str]] = Field(None, description="Lista de números de pedido") 