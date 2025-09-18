"""
Use case para enviar mensajes recordatorio de WhatsApp desde el API Gateway
"""
from typing import Optional, List
from datetime import datetime
import httpx
import json
from commons.api_client import APIClient, HTTPError
from commons.config import config
from api_gateway.domain.notification.dto.requests.notification_requests import SendRememberMessageWhatsappRequest
from api_gateway.domain.notification.dto.responses.notification_responses import NotificationResponse
from api_gateway.domain.reservation.dto.requests.reservation_filter_request import ReservationFilterRequest
from api_gateway.domain.reservation.dto.responses.reservation_response import ReservationResponse


class SendRememberMessageWhatsappUseCase:
    """Use case para enviar mensajes recordatorio de WhatsApp"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
        self.api_url = "https://api.p.2chat.io/open/whatsapp/send-message"
        self.api_key = "UAK74b4759f-68ae-4dc2-8925-06300085ec05"  # User provided API key
        self.from_number = "+595981048477"  # User provided from_number
    
    async def execute(self, request: SendRememberMessageWhatsappRequest, access_token: str = "") -> NotificationResponse:
        """
        Enviar mensaje recordatorio de WhatsApp para todas las reservas de la fecha
        
        Args:
            request: DTO con la fecha actual para recordatorios
            access_token: Token de acceso para autenticación
            
        Returns:
            NotificationResponse: Respuesta con el resultado de la operación
        """
        try:
            print(f"🔍 Buscando reservas para la fecha: {request.currentDate}")
            
            # 1. Obtener reservas de la fecha específica
            reservations = await self._get_reservations_for_date(request.currentDate, access_token)
            
            if not reservations:
                return NotificationResponse(
                    success=True,
                    message=f"No se encontraron reservas para la fecha: {request.currentDate}"
                )
            
            print(f"📋 Encontradas {len(reservations)} reservas para enviar recordatorios")
            
            # 2. Enviar mensajes para cada reserva
            success_count = 0
            error_count = 0
            error_messages = []
            
            for reservation in reservations:
                try:
                    # Verificar que la reserva tenga los datos necesarios
                    if not self._validate_reservation_data(reservation):
                        error_count += 1
                        error_msg = f"Reserva ID {reservation.id}: Datos incompletos"
                        error_messages.append(error_msg)
                        print(f"❌ {error_msg}")
                        continue
                    
                    # Construir mensaje
                    message = self._build_reminder_message(reservation)
                    
                    # Obtener número de teléfono del cliente
                    phone_number = self._get_customer_phone(reservation)
                    if not phone_number:
                        error_count += 1
                        error_msg = f"Reserva ID {reservation.id}: Sin número de teléfono"
                        error_messages.append(error_msg)
                        print(f"❌ {error_msg}")
                        continue
                    
                    # Enviar mensaje
                    success = await self._send_whatsapp_message(phone_number, message)
                    
                    if success:
                        success_count += 1
                        print(f"✅ Mensaje enviado exitosamente para reserva ID {reservation.id} - Cliente: {reservation.customer_data.company_name}")
                    else:
                        error_count += 1
                        error_msg = f"Reserva ID {reservation.id}: Error enviando mensaje"
                        error_messages.append(error_msg)
                        print(f"❌ {error_msg}")
                        
                except Exception as e:
                    error_count += 1
                    error_msg = f"Reserva ID {reservation.id}: {str(e)}"
                    error_messages.append(error_msg)
                    print(f"❌ {error_msg}")
            
            # 3. Construir respuesta final
            if success_count > 0:
                message = f"Proceso completado: {success_count} mensajes enviados exitosamente"
                if error_count > 0:
                    message += f", {error_count} errores"
                return NotificationResponse(
                    success=True,
                    message=message
                )
            else:
                return NotificationResponse(
                    success=False,
                    message=f"Error: No se pudo enviar ningún mensaje. Errores: {'; '.join(error_messages[:3])}"
                )
                
        except Exception as e:
            print(f"❌ Error inesperado en send_remember_message: {e}")
            return NotificationResponse(
                success=False,
                message=f"Error inesperado enviando mensajes recordatorio: {str(e)}"
            )
    
    async def _get_reservations_for_date(self, date_str: str, access_token: str) -> List[ReservationResponse]:
        """Obtener todas las reservas de una fecha específica"""
        try:
            # Parsear la fecha
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Construir filtro para obtener reservas de esa fecha
            filter_request = ReservationFilterRequest(
                start_date=date_str,
                end_date=date_str,
                skip=0,
                limit=1000  # Obtener todas las reservas de la fecha
            )
            
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/reservations/",
                    params={
                        "reservation_date_from": date_str,
                        "reservation_date_to": date_str,
                        "page": 1,
                        "limit": 1000
                    },
                    headers=headers
                )
                
                if response and "items" in response:
                    reservations = [ReservationResponse(**reservation) for reservation in response["items"]]
                    print(f"📊 Obtenidas {len(reservations)} reservas para {date_str}")
                    return reservations
                
                return []
                
        except Exception as e:
            print(f"❌ Error obteniendo reservas: {e}")
            return []
    
    def _validate_reservation_data(self, reservation: ReservationResponse) -> bool:
        """Validar que la reserva tenga todos los datos necesarios"""
        required_fields = [
            reservation.branch_data and reservation.branch_data.name,
            reservation.sector_data and reservation.sector_data.name,
            reservation.customer_data and reservation.customer_data.company_name,
            reservation.reason,
            reservation.unloading_time_minutes,
            reservation.start_time,
            reservation.branch_data and reservation.branch_data.ramp_name
        ]
        
        return all(required_fields)
    
    def _build_reminder_message(self, reservation: ReservationResponse) -> str:
        """Construir el mensaje recordatorio según el formato especificado"""
        # Formatear fecha y hora
        start_time_str = reservation.start_time.strftime("%d-%m-%Y %H:%M")
        
        # Formatear tiempo de descarga en horas
        unloading_hours = reservation.unloading_time_minutes / 60
        
        message = f"""Su reserva ha sido confirmada en {reservation.branch_data.name}
{reservation.reason}
Tiempo de descarga: {unloading_hours:.1f} h
Sector: {reservation.sector_data.name}
Fecha: {start_time_str}
Rampa: {reservation.branch_data.ramp_name}
Para duda o consulta, por favor contacte
IMPREVISTOS EN ENTREGA
SAC: +595 986 200006"""
        
        return message
    
    def _get_customer_phone(self, reservation: ReservationResponse) -> Optional[str]:
        """Obtener el número de teléfono del cliente"""
        if not reservation.customer_data:
            return None
        
        # Priorizar celular sobre teléfono fijo
        if reservation.customer_data.cellphone_number:
            # Agregar código de país si no está presente
            phone = reservation.customer_data.cellphone_number
            if not phone.startswith('+'):
                country_code = reservation.customer_data.cellphone_country_code or "+595"
                phone = f"{country_code}{phone}"
            return phone
        
        if reservation.customer_data.phone:
            return reservation.customer_data.phone
        
        return None
    
    async def _send_whatsapp_message(self, to_number: str, text: str) -> bool:
        """Enviar mensaje de WhatsApp usando 2Chat API"""
        try:
            payload = {
                "to_number": to_number,
                "from_number": self.from_number,
                "text": text,
            }
            
            headers = {
                'X-User-API-Key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
            
            if response.status_code in [200, 202]:
                response_data = response.json()
                if response_data.get("success") or response_data.get("status") == "success":
                    return True
                else:
                    print(f"❌ Error en 2Chat API: {response_data.get('message', 'Error desconocido')}")
                    return False
            else:
                print(f"❌ Error HTTP {response.status_code}: {response.text}")
                return False
                
        except httpx.TimeoutException:
            print("❌ Error de timeout: La API de 2Chat no respondió en 30 segundos")
            return False
        except httpx.RequestError as e:
            print(f"❌ Error de conexión con 2Chat API: {str(e)}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error parseando respuesta de 2Chat API: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado enviando mensaje: {str(e)}")
            return False
