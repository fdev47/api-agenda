"""
Entidad para datos de sucursal
"""
from dataclasses import dataclass


@dataclass
class BranchData:
    """Datos de la sucursal al momento de la reserva"""
    # ID de referencia en location_service
    branch_id: int
    # Datos completos al momento de la reserva
    name: str
    code: str
    address: str
    country_id: int
    country_name: str
    state_id: int
    state_name: str
    city_id: int
    city_name: str
    ramp_id: int
    ramp_name: str 