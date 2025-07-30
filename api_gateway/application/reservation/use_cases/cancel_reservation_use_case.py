"""
Use case para cancelar reservas desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.reservation.dto.responses.reservation_response import ReservationResponse


class CancelReservationUseCase:
    """Use case para cancelar reservas usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, reservation_id: int, access_token: str = "") -> ReservationResponse:
        """
        Cancelar reserva desde el reservation_service
        
        Args:
            reservation_id: ID de la reserva a cancelar
            access_token: Token de acceso para autenticación
            
        Returns:
            ReservationResponse: Reserva cancelada
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.delete(
                    f"{config.API_PREFIX}/reservations/{reservation_id}",
                    headers=headers
                )
                
                if response:
                    return ReservationResponse(**response)
                
                raise Exception("Error cancelando reserva")
                
        except Exception as e:
            print(f"Error cancelando reserva: {e}")
            raise e 