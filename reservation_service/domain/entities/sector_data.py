"""
Entidad para datos de sector
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SectorData:
    """Datos del sector al momento de la reserva"""
    # ID de referencia en location_service
    sector_id: int
    # Datos completos al momento de la reserva
    name: str
    sector_type_id: int
    sector_type_name: str
    measurement_unit_id: int
    measurement_unit_name: str
    description: Optional[str] = None
    capacity: Optional[float] = None
    
    # Nuevos campos para cantidades
    pallet_count: int = 0
    granel_count: int = 0
    boxes_count: int = 0 