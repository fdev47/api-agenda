"""
Request DTO para datos del cliente
"""
from pydantic import BaseModel, Field
from typing import Optional


class CustomerDataRequest(BaseModel):
    """Request para datos del cliente"""
    # ID de referencia (opcional, puede no existir en el sistema)
    customer_id: Optional[int] = Field(None, gt=0, description="ID del cliente en el sistema")
    # Datos completos al momento de la reserva
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del cliente")
    email: str = Field(..., description="Email del cliente")
    phone: str = Field(..., min_length=7, max_length=20, description="Número de teléfono") 