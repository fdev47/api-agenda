"""
Response DTO para datos de sector
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class SectorDataResponse(BaseModel):
    """Response para datos del sector"""
    # ID de referencia en location_service
    sector_id: int = Field(..., description="ID del sector")
    # Datos completos al momento de la reserva
    name: str = Field(..., description="Nombre del sector")
    description: Optional[str] = Field(None, description="Descripción del sector")
    sector_type_id: int = Field(..., description="ID del tipo de sector")
    sector_type_name: str = Field(..., description="Nombre del tipo de sector")
    capacity: Optional[float] = Field(None, description="Capacidad del sector")
    measurement_unit_id: int = Field(..., description="ID de la unidad de medida")
    measurement_unit_name: str = Field(..., description="Nombre de la unidad de medida")
    
    # Nuevos campos para cantidades (opcionales para compatibilidad con reservas existentes)
    pallet_count: int = Field(0, description="Cantidad de palets")
    granel_count: int = Field(0, description="Cantidad de graneles")
    boxes_count: int = Field(0, description="Cantidad de cajas")
    
    # Números de pedido asociados
    order_numbers: Optional[List[str]] = Field(None, description="Lista de números de pedido") 