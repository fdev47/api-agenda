"""
Use case para crear reservas desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.reservation.dto.requests.create_reservation_request import CreateReservationRequest
from ....domain.reservation.dto.responses.reservation_response import ReservationResponse


class CreateReservationUseCase:
    """Use case para crear reservas usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, request: CreateReservationRequest, access_token: str = "") -> ReservationResponse:
        """
        Crear reserva desde el reservation_service
        
        Args:
            request: DTO con los datos de la reserva
            access_token: Token de acceso para autenticación
            
        Returns:
            ReservationResponse: Reserva creada
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                # El DTO ya tiene método dict() personalizado que convierte datetime
                response = await client.post(
                    f"{config.API_PREFIX}/reservations/",
                    data=request.dict(),
                    headers=headers
                )
                
                if response:
                    return ReservationResponse(**response)
                
                raise Exception("Error creando reserva")
                
        except Exception as e:
            print(f"Error creando reserva: {e}")
            raise e 