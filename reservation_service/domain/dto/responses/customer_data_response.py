"""
Response DTO para datos del cliente
"""
from pydantic import BaseModel, Field
from typing import Optional


class CustomerDataResponse(BaseModel):
    """Response para datos del cliente"""
    # ID de referencia (opcional, puede no existir en el sistema)
    customer_id: Optional[int] = Field(None, description="ID del cliente en el sistema")
    # Datos completos al momento de la reserva
    name: str = Field(..., description="Nombre del cliente")
    email: str = Field(..., description="Email del cliente")
    phone: str = Field(..., description="Número de teléfono") 