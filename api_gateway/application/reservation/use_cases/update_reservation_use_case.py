"""
Use case para actualizar reservas desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.reservation.dto.requests.update_reservation_request import UpdateReservationRequest
from ....domain.reservation.dto.responses.reservation_response import ReservationResponse


class UpdateReservationUseCase:
    """Use case para actualizar reservas usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, reservation_id: int, request: UpdateReservationRequest, access_token: str = "") -> ReservationResponse:
        """
        Actualizar reserva desde el reservation_service
        
        Args:
            reservation_id: ID de la reserva a actualizar
            request: DTO con los datos de actualización
            access_token: Token de acceso para autenticación
            
        Returns:
            ReservationResponse: Reserva actualizada
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                # El DTO ya tiene método dict() personalizado que convierte datetime
                response = await client.put(
                    f"{config.API_PREFIX}/reservations/{reservation_id}",
                    data=request.dict(exclude_none=True),
                    headers=headers
                )
                
                if response:
                    return ReservationResponse(**response)
                
                raise Exception("Error actualizando reserva")
                
        except Exception as e:
            print(f"Error actualizando reserva: {e}")
            raise e 