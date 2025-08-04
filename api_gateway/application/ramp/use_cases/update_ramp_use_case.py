"""
Caso de uso para actualizar rampa en API Gateway
"""
import logging
from commons.api_client import HTTPError, APIClient
from commons.config import config
from ....domain.ramp.dto.requests.update_ramp_request import UpdateRampRequest
from ....domain.ramp.dto.responses.ramp_response import RampResponse

logger = logging.getLogger(__name__)


class UpdateRampUseCase:
    """Caso de uso para actualizar una rampa"""
    
    def __init__(self):
        self.location_client = APIClient(base_url=config.LOCATION_SERVICE_URL)
    
    async def execute(self, ramp_id: int, update_request: UpdateRampRequest, access_token: str = "") -> RampResponse:
        """
        Ejecutar el caso de uso para actualizar una rampa
        
        Args:
            ramp_id: ID de la rampa a actualizar
            update_request: Datos de la rampa a actualizar
            access_token: Token de acceso para autenticación
            
        Returns:
            RampResponse: Rampa actualizada
            
        Raises:
            HTTPError: Si hay errores en el servicio de ubicación
        """
        logger.info(f"🚀 Ejecutando UpdateRampUseCase para rampa {ramp_id}")
        
        # Usar context manager para el cliente HTTP
        async with self.location_client as location_client:
            # Llamar al servicio de ubicación para actualizar la rampa
            logger.info(f"📞 Llamando al location_service para actualizar rampa {ramp_id}")
            
            result = await location_client.put(
                f"{config.API_PREFIX}/ramps/{ramp_id}",
                data=update_request.dict(exclude_unset=True),
                headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
            )
            
            logger.info(f"✅ Rampa {ramp_id} actualizada exitosamente")
            
            # Convertir la respuesta a RampResponse
            return RampResponse(**result) 