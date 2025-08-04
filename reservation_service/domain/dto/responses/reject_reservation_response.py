"""
Response DTO para rechazo de reserva en Reservation Service
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RejectReservationResponse(BaseModel):
    """Response para datos de rechazo de una reserva"""
    
    user_id: str = Field(..., description="ID del usuario que rechaza la reserva")
    user_name: str = Field(..., description="Nombre del usuario que rechaza la reserva")
    date: datetime = Field(..., description="Fecha y hora del rechazo")
    reason: str = Field(..., min_length=10, max_length=500, description="Motivo del rechazo")
    comment: Optional[str] = Field(None, max_length=1000, description="Comentario adicional del rechazo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "12345",
                "user_name": "Juan Pérez",
                "date": "2025-08-03T22:50:00",
                "reason": "No hay disponibilidad de horario para la fecha solicitada",
                "comment": "El cliente debe contactar para reagendar en otra fecha"
            }
        } 