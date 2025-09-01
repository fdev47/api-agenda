"""
Use case para enviar mensajes de WhatsApp desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient, HTTPError
from commons.config import config
from api_gateway.domain.notification.dto.requests.notification_requests import SendMessageWhatsappRequest
from api_gateway.domain.notification.dto.responses.notification_responses import NotificationResponse


class SendMessageWhatsappUseCase:
    """Use case para enviar mensajes de WhatsApp"""
    
    def __init__(self):
        # TODO: Configurar URL del servicio de notificaciones cuando esté disponible
        self.notification_service_url = "http://localhost:8003"  # Placeholder
    
    async def execute(self, request: SendMessageWhatsappRequest, access_token: str = "") -> NotificationResponse:
        """
        Enviar mensaje de WhatsApp
        
        Args:
            request: DTO con los datos del mensaje
            access_token: Token de acceso para autenticación
            
        Returns:
            NotificationResponse: Respuesta con el resultado de la operación
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            # TODO: Implementar cuando el servicio de notificaciones esté disponible
            # Por ahora retornamos una respuesta simulada
            return NotificationResponse(
                success=True,
                message="Mensaje de WhatsApp enviado exitosamente (simulado)"
            )
            
            # Código para cuando el servicio esté disponible:
            # async with APIClient(self.notification_service_url, "") as client:
            #     response = await client.post(
            #         f"{config.API_PREFIX}/notifications/send-whatsapp",
            #         data=request.dict(),
            #         headers=headers
            #     )
            #     
            #     if response:
            #         return NotificationResponse(
            #             success=response.get("success", True),
            #             message=response.get("message", "Mensaje enviado exitosamente")
            #         )
            #     
            #     return NotificationResponse(
            #         success=False,
            #         message="Error enviando mensaje"
            #         )
                
        except HTTPError as e:
            print(f"Error HTTP enviando mensaje: {e}")
            raise e
        except Exception as e:
            print(f"Error inesperado enviando mensaje: {e}")
            return NotificationResponse(
                success=False,
                message=f"Error enviando mensaje: {str(e)}"
            )
