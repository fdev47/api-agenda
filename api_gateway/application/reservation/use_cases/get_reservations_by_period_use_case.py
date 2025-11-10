"""
Use case para obtener reservas por período desde el API Gateway
"""
import logging
from commons.api_client import APIClient, HTTPError
from commons.config import config
from ....domain.reservation.dto.requests.reservation_period_request import ReservationPeriodRequest
from ....domain.reservation.dto.responses.reservation_period_response import ReservationPeriodResponse

logger = logging.getLogger(__name__)


class GetReservationsByPeriodUseCase:
    """Use case para obtener reservas por período usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, request: ReservationPeriodRequest, access_token: str = "") -> ReservationPeriodResponse:
        """
        Obtener reservas por período desde el reservation_service
        
        Args:
            request: Request con parámetros de búsqueda (branch_id, start_time, end_time, status)
            access_token: Token de acceso para autenticación
            
        Returns:
            ReservationPeriodResponse: Lista de reservas en el período
        """
        try:
            logger.info(f"📅 API Gateway - Obteniendo reservas por período: branch_id={request.branch_id}")
            
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            # Construir query params
            params = {
                "branch_id": request.branch_id,
                "start_time": request.start_time.isoformat(),
                "end_time": request.end_time.isoformat()
            }
            
            if request.status:
                params["status"] = request.status
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/reservations/period",
                    params=params,
                    headers=headers
                )
                
                if response:
                    logger.info(f"✅ Se obtuvieron {response.get('total', 0)} reservas del reservation_service")
                    return ReservationPeriodResponse(**response)
                
                raise Exception("Error al obtener reservas por período")
                
        except HTTPError as e:
            logger.error(f"❌ Error HTTP obteniendo reservas por período: {e}")
            raise e
        except Exception as e:
            logger.error(f"❌ Error inesperado obteniendo reservas por período: {e}")
            raise e

