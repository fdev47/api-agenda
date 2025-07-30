"""
DTO de response para lista de reservas en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import List
from .reservation_response import ReservationResponse


class ReservationListResponse(BaseModel):
    """DTO para lista de reservas"""
    reservations: List[ReservationResponse] = Field(..., description="Lista de reservas")
    total: int = Field(..., description="Total de reservas")
    skip: int = Field(..., description="Número de elementos omitidos")
    limit: int = Field(..., description="Límite de elementos por página") 