"""
Use case para actualizar main_reservations desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient, HTTPError
from commons.config import config
from ....domain.reservation.dto.requests.update_main_reservation_request import UpdateMainReservationRequest
from ....domain.reservation.dto.responses.main_reservation_response import MainReservationResponse


class UpdateMainReservationUseCase:
    """Use case para actualizar main_reservations usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, request: UpdateMainReservationRequest, access_token: str = "") -> MainReservationResponse:
        """
        Actualizar main_reservation desde el reservation_service
        
        Args:
            request: DTO con los datos actualizados de la main_reservation
            access_token: Token de acceso para autenticación
            
        Returns:
            MainReservationResponse: Main_reservation actualizada
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.put(
                    f"{config.API_PREFIX}/main-reservations/{request.id}",
                    data=request.dict(),
                    headers=headers
                )
                
                if response:
                    return MainReservationResponse(**response)
                
                raise Exception("Error actualizando main_reservation")
                
        except HTTPError as e:
            print(f"Error HTTP actualizando main_reservation: {e}")
            raise e
        except Exception as e:
            print(f"Error inesperado actualizando main_reservation: {e}")
            raise e

