"""
Use case para enviar mensajes de WhatsApp desde el API Gateway
"""
import httpx
import json
from typing import Optional
from commons.api_client import APIClient, HTTPError
from commons.config import config
from api_gateway.domain.notification.dto.requests.notification_requests import SendMessageWhatsappRequest
from api_gateway.domain.notification.dto.responses.notification_responses import NotificationResponse


class SendMessageWhatsappUseCase:
    """Use case para enviar mensajes de WhatsApp usando 2Chat API"""
    
    def __init__(self):
        # Configuración de 2Chat API
        self.api_url = "https://api.p.2chat.io/open/whatsapp/send-message"
        # TODO: Agregar API key en variables de entorno
        self.api_key = "UAK74b4759f-68ae-4dc2-8925-06300085ec05"
    
    async def execute(self, request: SendMessageWhatsappRequest, access_token: str = "") -> NotificationResponse:
        """
        Enviar mensaje de WhatsApp usando 2Chat API
        
        Args:
            request: DTO con los datos del mensaje
            access_token: Token de acceso para autenticación (no usado por 2Chat)
            
        Returns:
            NotificationResponse: Respuesta con el resultado de la operación
        """
        try:
            # Preparar payload para 2Chat API
            payload = {
                "to_number": request.to_number,
                "from_number": request.from_number,
                "text": request.text,
            }
            
            # Headers para 2Chat API
            headers = {
                'X-User-API-Key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            # Enviar request usando httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
            
            # Procesar respuesta
            if response.status_code in [200, 202]:  # Aceptar tanto 200 OK como 202 Accepted
                response_data = response.json()
                
                # Verificar si el mensaje se envió exitosamente según la respuesta de 2Chat
                if response_data.get("success") or response_data.get("status") == "success":
                    return NotificationResponse(
                        success=True,
                        message=f"Mensaje de WhatsApp enviado exitosamente a {request.to_number}"
                    )
                else:
                    error_msg = response_data.get("message", "Error desconocido en 2Chat API")
                    return NotificationResponse(
                        success=False,
                        message=f"Error en 2Chat API: {error_msg}"
                    )
            else:
                # Error HTTP
                error_msg = f"Error HTTP {response.status_code}: {response.text}"
                return NotificationResponse(
                    success=False,
                    message=f"Error enviando mensaje: {error_msg}"
                )
                
        except httpx.TimeoutException:
            # Error de timeout
            return NotificationResponse(
                success=False,
                message="Error de timeout: La API de 2Chat no respondió en 30 segundos"
            )
        except httpx.RequestError as e:
            # Error de red o conexión
            return NotificationResponse(
                success=False,
                message=f"Error de conexión con 2Chat API: {str(e)}"
            )
        except json.JSONDecodeError as e:
            # Error parseando respuesta JSON
            return NotificationResponse(
                success=False,
                message=f"Error parseando respuesta de 2Chat API: {str(e)}"
            )
        except Exception as e:
            # Error inesperado
            return NotificationResponse(
                success=False,
                message=f"Error inesperado enviando mensaje: {str(e)}"
            )
