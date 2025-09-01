"""
DTOs de responses para notificaciones en el API Gateway

Este módulo contiene todos los DTOs de respuesta necesarios para la gestión de notificaciones
a través del API Gateway.
"""
from pydantic import BaseModel, Field


class NotificationResponse(BaseModel):
    """DTO para respuesta de notificaciones"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de la operación")
