"""
Caso de uso para eliminar rampa en API Gateway
"""
import logging
from commons.api_client import HTTPError, APIClient
from commons.config import config
from ....domain.ramp.dto.responses.ramp_response import RampResponse

logger = logging.getLogger(__name__)


class DeleteRampUseCase:
    """Caso de uso para eliminar una rampa"""
    
    def __init__(self):
        self.location_client = APIClient(base_url=config.LOCATION_SERVICE_URL)
    
    async def execute(self, ramp_id: int, access_token: str = "") -> RampResponse:
        """
        Ejecutar el caso de uso para eliminar una rampa
        
        Args:
            ramp_id: ID de la rampa a eliminar
            access_token: Token de acceso para autenticación
            
        Returns:
            RampResponse: Rampa eliminada
            
        Raises:
            HTTPError: Si hay errores en el servicio de ubicación
        """
        logger.info(f"🚀 Ejecutando DeleteRampUseCase para rampa {ramp_id}")
        
        # Usar context manager para el cliente HTTP
        async with self.location_client as location_client:
            # Llamar al servicio de ubicación para eliminar la rampa
            logger.info(f"📞 Llamando al location_service para eliminar rampa {ramp_id}")
            
            result = await location_client.delete(
                f"{config.API_PREFIX}/ramps/{ramp_id}",
                headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
            )
            
            logger.info(f"✅ Rampa {ramp_id} eliminada exitosamente")
            
            # Convertir la respuesta a RampResponse
            return RampResponse(**result) 