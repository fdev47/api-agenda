"""
Response DTO para lista de resúmenes de reservas
"""
from pydantic import BaseModel, Field
from typing import List

from .reservation_summary_response import ReservationSummaryResponse


class ReservationSummaryListResponse(BaseModel):
    """Response para lista resumida de reservas"""
    items: List[ReservationSummaryResponse] = Field(..., description="Lista de reservas resumidas")
    total: int = Field(..., description="Total de reservas")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de la página")
    pages: int = Field(..., description="Total de páginas") 