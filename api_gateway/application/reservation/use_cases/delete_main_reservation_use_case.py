"""
Use case para eliminar main_reservations desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient, HTTPError
from commons.config import config
from ....domain.reservation.dto.responses.main_reservation_response import MainReservationResponse


class DeleteMainReservationUseCase:
    """Use case para eliminar main_reservations usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, main_reservation_id: int, access_token: str = "") -> MainReservationResponse:
        """
        Eliminar main_reservation desde el reservation_service
        
        Args:
            main_reservation_id: ID de la main_reservation
            access_token: Token de acceso para autenticación
            
        Returns:
            MainReservationResponse: Main_reservation eliminada
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.delete(
                    f"{config.API_PREFIX}/main-reservations/{main_reservation_id}",
                    headers=headers
                )
                
                if response:
                    return MainReservationResponse(**response)
                
                raise Exception("Error eliminando main_reservation")
                
        except HTTPError as e:
            print(f"Error HTTP eliminando main_reservation: {e}")
            raise e
        except Exception as e:
            print(f"Error inesperado eliminando main_reservation: {e}")
            raise e

