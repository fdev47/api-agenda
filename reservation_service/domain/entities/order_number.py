"""
Entidad para números de pedido
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderNumber:
    """Número de pedido con su código"""
    code: str
    description: Optional[str] = None 