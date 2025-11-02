"""
Use case para crear main_reservations desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient, HTTPError
from commons.config import config
from ....domain.reservation.dto.requests.create_main_reservation_request import CreateMainReservationRequest
from ....domain.reservation.dto.responses.main_reservation_response import MainReservationResponse


class CreateMainReservationUseCase:
    """Use case para crear main_reservations usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, request: CreateMainReservationRequest, access_token: str = "") -> MainReservationResponse:
        """
        Crear main_reservation desde el reservation_service
        
        Args:
            request: DTO con los datos de la main_reservation
            access_token: Token de acceso para autenticación
            
        Returns:
            MainReservationResponse: Main_reservation creada
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.post(
                    f"{config.API_PREFIX}/main-reservations/",
                    data=request.dict(),
                    headers=headers
                )
                
                if response:
                    return MainReservationResponse(**response)
                
                raise Exception("Error creando main_reservation")
                
        except HTTPError as e:
            print(f"Error HTTP creando main_reservation: {e}")
            raise e
        except Exception as e:
            print(f"Error inesperado creando main_reservation: {e}")
            raise e

