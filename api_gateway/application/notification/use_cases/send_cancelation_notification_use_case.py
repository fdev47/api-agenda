"""
Use case para enviar notificaciones de cancelación de reserva
"""
import logging
from typing import List, Optional
from commons.api_client import APIClient, HTTPError
from commons.config import config
from api_gateway.domain.notification.dto.requests.notification_requests import (
    SendCancelationNotificationRequest,
    SendMessageWhatsappRequest
)
from api_gateway.domain.notification.dto.responses.notification_responses import NotificationResponse
from api_gateway.application.notification.use_cases.send_message_whatsapp_use_case import SendMessageWhatsappUseCase
from api_gateway.application.reservation.use_cases.get_reservation_use_case import GetReservationUseCase

# Configurar logger
logger = logging.getLogger(__name__)


class SendCancelationNotificationUseCase:
    """Use case para enviar notificaciones de cancelación de reserva a administradores"""
    
    def __init__(self):
        self.whatsapp_use_case = SendMessageWhatsappUseCase()
        # Número de origen para WhatsApp (puede ser configurado en variables de entorno)
        self.from_number = "+595974731211"  # TODO: Mover a configuración
    
    async def execute(self, request: SendCancelationNotificationRequest, access_token: str = "") -> NotificationResponse:
        """
        Enviar notificación de cancelación de reserva
        
        Args:
            request: DTO con el ID de la reserva cancelada
            access_token: Token de acceso para autenticación
            
        Returns:
            NotificationResponse: Respuesta con el resultado de la operación
        """
        try:
            logger.info(f"🚀 Iniciando notificación de cancelación para reserva: {request.reservation_id}")
            
            # 1. Recuperar los datos de detalle de reserva usando el API Gateway interno
            get_reservation_use_case = GetReservationUseCase()
            reservation_detail = await get_reservation_use_case.execute(request.reservation_id, access_token)
            
            if not reservation_detail:
                return NotificationResponse(
                    success=False,
                    message=f"No se pudo obtener los datos de la reserva {request.reservation_id}"
                )
            
            logger.info(f"✅ Datos de reserva obtenidos: {reservation_detail.customer_data.company_name if reservation_detail.customer_data else 'N/A'}")
            
            # 2. Extraer el código de branch directamente de los datos de la reserva
            branch_code = None
            if reservation_detail.branch_data and reservation_detail.branch_data.code:
                branch_code = reservation_detail.branch_data.code
            
            if not branch_code:
                return NotificationResponse(
                    success=False,
                    message=f"No se pudo obtener el código de branch para la reserva {request.reservation_id}"
                )
            
            logger.info(f"✅ Código de branch obtenido: {branch_code}")
            
            # 3. Obtener todos los usuarios admin con branch_code
            admin_users = await self._get_admin_users_by_branch(branch_code, access_token)
            if not admin_users:
                return NotificationResponse(
                    success=False,
                    message=f"No se encontraron usuarios administradores para el branch {branch_code}"
                )
            
            logger.info(f"✅ Se encontraron {len(admin_users)} usuarios administradores")
            
            # 4. Preparar mensaje de cancelación
            company_name = reservation_detail.customer_data.company_name if reservation_detail.customer_data else 'Cliente desconocido'
            start_date = reservation_detail.start_time.strftime("%Y-%m-%d") if reservation_detail.start_time else 'N/A'
            start_time = reservation_detail.start_time.strftime("%H:%M") if reservation_detail.start_time else 'N/A'
            message_text = f"CANCELACIÓN DE RESERVA\n\nLa reserva ha sido cancelada por: {company_name}\n\nReserva ID: {request.reservation_id}\n\nFecha: {start_date}\nHora: {start_time} hs"
            
            # 5. Enviar mensaje a todos los usuarios admin
            successful_sends = 0
            failed_sends = 0
            
            for user in admin_users:
                phone = user.get('phone')
                if phone:
                    try:
                        whatsapp_request = SendMessageWhatsappRequest(
                            to_number=phone,
                            from_number=self.from_number,
                            text=message_text
                        )
                        
                        print(f"🔄 Enviando mensaje a {whatsapp_request}: {message_text}")
                        result = await self.whatsapp_use_case.execute(whatsapp_request, access_token)
                        
                        if result.success:
                            successful_sends += 1
                            logger.info(f"✅ Mensaje enviado exitosamente a {phone}")
                        else:
                            failed_sends += 1
                            logger.warning(f"❌ Error enviando mensaje a {phone}: {result.message}")
                    
                    except Exception as e:
                        failed_sends += 1
                        logger.error(f"❌ Error inesperado enviando mensaje a {phone}: {str(e)}")
                else:
                    failed_sends += 1
                    logger.warning(f"❌ Usuario sin teléfono: {user.get('email', 'N/A')}")
            
            # Preparar respuesta final
            if successful_sends > 0:
                message = f"Notificación enviada exitosamente a {successful_sends} administradores"
                if failed_sends > 0:
                    message += f" (falló en {failed_sends} envíos)"
                
                return NotificationResponse(
                    success=True,
                    message=message
                )
            else:
                return NotificationResponse(
                    success=False,
                    message=f"No se pudo enviar la notificación a ningún administrador ({failed_sends} fallos)"
                )
            
        except Exception as e:
            logger.error(f"❌ Error inesperado en notificación de cancelación: {str(e)}")
            return NotificationResponse(
                success=False,
                message=f"Error inesperado: {str(e)}"
            )
    
    
    async def _get_admin_users_by_branch(self, branch_code: str, access_token: str) -> List[dict]:
        """Obtener todos los usuarios admin con branch_code desde user_service"""
        try:
            logger.info(f"📞 Consultando usuarios admin para branch: {branch_code}")
            
            async with APIClient(config.USER_SERVICE_URL, access_token) as client:
                # Buscar usuarios admin con el branch_code específico
                params = {
                    "role": "admin",
                    "branch_code": branch_code
                }
                response = await client.get("/api/v1/users", params=params)
                
                users = response.get('users', []) if isinstance(response, dict) else response
                logger.info(f"✅ Se encontraron {len(users)} usuarios admin")
                return users
                
        except HTTPError as e:
            logger.error(f"❌ Error HTTP obteniendo usuarios admin: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error inesperado obteniendo usuarios admin: {str(e)}")
            return []

