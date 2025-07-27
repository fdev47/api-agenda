"""
Response DTO para lista de reservas
"""
from pydantic import BaseModel, Field
from typing import List

from .reservation_response import ReservationResponse


class ReservationListResponse(BaseModel):
    """Response para lista de reservas con paginación"""
    items: List[ReservationResponse] = Field(..., description="Lista de reservas")
    total: int = Field(..., description="Total de reservas")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de la página")
    pages: int = Field(..., description="Total de páginas") 