"""
DTOs de requests para notificaciones en el API Gateway

Este módulo contiene todos los DTOs de solicitud necesarios para la gestión de notificaciones
a través del API Gateway. Los DTOs incluyen validaciones y ejemplos para mejorar la 
documentación de Swagger.

Campos principales:
- to_number: Número de teléfono destino
- from_number: Número de teléfono origen
- text: Mensaje de texto a enviar
- currentDate: Fecha actual para recordatorios
"""
from pydantic import BaseModel, Field


class SendMessageWhatsappRequest(BaseModel):
    """Solicitud para enviar mensaje de WhatsApp"""
    to_number: str = Field(..., description="Número de teléfono destino")
    from_number: str = Field(..., description="Número de teléfono origen")
    text: str = Field(..., description="Mensaje de texto a enviar")


class SendRememberMessageWhatsappRequest(BaseModel):
    """Solicitud para enviar mensaje recordatorio de WhatsApp"""
    currentDate: str = Field(..., description="Fecha actual para recordatorios")


class SendCancelationNotificationRequest(BaseModel):
    """Solicitud para enviar notificación de cancelación de reserva"""
    reservation_id: str = Field(..., description="ID de la reserva cancelada")
