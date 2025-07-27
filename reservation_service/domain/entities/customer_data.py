"""
Entidad para datos del cliente
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CustomerData:
    """Datos del cliente al momento de la reserva"""
    # Datos completos al momento de la reserva
    name: str
    email: str
    phone: str
    # ID de referencia (opcional, puede no existir en el sistema)
    customer_id: Optional[int] = None 