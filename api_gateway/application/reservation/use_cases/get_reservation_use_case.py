"""
Use case para obtener reservas desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient, HTTPError
from commons.config import config
from ....domain.reservation.dto.responses.reservation_response import ReservationResponse


class GetReservationUseCase:
    """Use case para obtener reservas usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, reservation_id: int, access_token: str = "") -> ReservationResponse:
        """
        Obtener reserva desde el reservation_service
        
        Args:
            reservation_id: ID de la reserva
            access_token: Token de acceso para autenticación
            
        Returns:
            ReservationResponse: Reserva obtenida
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/reservations/{reservation_id}",
                    headers=headers
                )
                
                if response:
                    return ReservationResponse(**response)
                
                raise Exception("Reserva no encontrada")
                
        except HTTPError as e:
            # Propagar errores HTTP directamente
            print(f"Error HTTP obteniendo reserva: {e}")
            raise e
        except Exception as e:
            print(f"Error inesperado obteniendo reserva: {e}")
            raise e 