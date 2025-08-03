"""
Caso de uso para rechazar una reserva en API Gateway
"""
import logging
from datetime import datetime
from typing import Optional
from commons.api_client import HTTPError, APIClient
from commons.config import config
from ....domain.reservation.dto.requests.reject_reservation_request import RejectReservationRequest
from ....domain.reservation.dto.responses.reservation_response import ReservationResponse

logger = logging.getLogger(__name__)


class RejectReservationUseCase:
    """Caso de uso para rechazar una reserva"""
    
    def __init__(self):
        self.reservation_client = APIClient(base_url=config.RESERVATION_SERVICE_URL)
    
    async def execute(self, reservation_id: int, reject_request: RejectReservationRequest, access_token: str = "") -> ReservationResponse:
        """
        Ejecutar el caso de uso para rechazar una reserva
        
        Args:
            reservation_id: ID de la reserva a rechazar
            reject_request: Datos del rechazo
            access_token: Token de acceso para autenticación
            
        Returns:
            ReservationResponse: Reserva actualizada
            
        Raises:
            HTTPError: Si hay errores en el servicio de reservas
        """
        logger.info(f"🚀 Ejecutando RejectReservationUseCase para reserva {reservation_id}")
        
        # Usar context manager para el cliente HTTP
        async with self.reservation_client as reservation_client:
            # Llamar al servicio de reservas para rechazar la reserva
            logger.info(f"📞 Llamando al reservation_service para rechazar reserva {reservation_id}")
            
            result = await reservation_client.post(
                f"{config.API_PREFIX}/reservations/{reservation_id}/cancel",
                data=reject_request.dict(),
                headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
            )
            
            logger.info(f"✅ Reserva {reservation_id} rechazada exitosamente")
            
            # Convertir la respuesta a ReservationResponse
            return ReservationResponse(**result) 