"""
Response DTO para completado de reserva en Reservation Service
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CompleteReservationResponse(BaseModel):
    """Response para datos de completado de una reserva"""
    
    user_id: str = Field(..., description="ID del usuario que completa la reserva")
    user_name: str = Field(..., description="Nombre del usuario que completa la reserva")
    date: datetime = Field(..., description="Fecha y hora de completado")
    download_time: str = Field(..., description="Tiempo de descarga")
    success_code: str = Field(..., description="Código de éxito")
    comment: Optional[str] = Field(None, max_length=1000, description="Comentario adicional del completado")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "12345",
                "user_name": "Juan Pérez",
                "date": "2025-08-03T22:50:00",
                "download_time": "2 horas 30 minutos",
                "success_code": "SUCCESS_001",
                "comment": "Descarga completada exitosamente"
            }
        } 