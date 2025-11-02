"""
Use case para obtener main_reservations desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient, HTTPError
from commons.config import config
from ....domain.reservation.dto.responses.main_reservation_response import MainReservationResponse


class GetMainReservationUseCase:
    """Use case para obtener main_reservations usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, main_reservation_id: int, access_token: str = "") -> MainReservationResponse:
        """
        Obtener main_reservation desde el reservation_service
        
        Args:
            main_reservation_id: ID de la main_reservation
            access_token: Token de acceso para autenticación
            
        Returns:
            MainReservationResponse: Main_reservation obtenida
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/main-reservations/{main_reservation_id}",
                    headers=headers
                )
                
                if response:
                    return MainReservationResponse(**response)
                
                raise Exception("Main_reservation no encontrada")
                
        except HTTPError as e:
            print(f"Error HTTP obteniendo main_reservation: {e}")
            raise e
        except Exception as e:
            print(f"Error inesperado obteniendo main_reservation: {e}")
            raise e

