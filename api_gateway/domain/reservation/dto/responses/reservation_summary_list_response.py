"""
DTO de response para lista de resúmenes de reservas en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import List
from .reservation_summary_response import ReservationSummaryResponse


class ReservationSummaryListResponse(BaseModel):
    """DTO para lista de resúmenes de reservas"""
    reservations: List[ReservationSummaryResponse] = Field(..., description="Lista de resúmenes de reservas")
    total: int = Field(..., description="Total de reservas")
    skip: int = Field(..., description="Número de elementos omitidos")
    limit: int = Field(..., description="Límite de elementos por página") 