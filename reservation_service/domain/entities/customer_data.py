"""
Entidad para datos del cliente
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class CustomerData:
    """Datos del cliente al momento de la reserva"""
    # Campos obligatorios
    ruc: str
    company_name: str
    email: str
    
    # Campos opcionales
    customer_id: Optional[int] = None
    id: Optional[UUID] = None
    auth_uid: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    cellphone_number: Optional[str] = None
    cellphone_country_code: Optional[str] = None
    address_id: Optional[UUID] = None
    is_active: bool = True 