"""
Caso de uso para crear rampa en API Gateway
"""
import logging
from commons.api_client import HTTPError, APIClient
from commons.config import config
from ....domain.ramp.dto.requests.create_ramp_request import CreateRampRequest
from ....domain.ramp.dto.responses.ramp_response import RampResponse

logger = logging.getLogger(__name__)


class CreateRampUseCase:
    """Caso de uso para crear una rampa"""
    
    def __init__(self):
        self.location_client = APIClient(base_url=config.LOCATION_SERVICE_URL)
    
    async def execute(self, create_request: CreateRampRequest, access_token: str = "") -> RampResponse:
        """
        Ejecutar el caso de uso para crear una rampa
        
        Args:
            create_request: Datos de la rampa a crear
            access_token: Token de acceso para autenticación
            
        Returns:
            RampResponse: Rampa creada
            
        Raises:
            HTTPError: Si hay errores en el servicio de ubicación
        """
        logger.info(f"🚀 Ejecutando CreateRampUseCase")
        
        # Usar context manager para el cliente HTTP
        async with self.location_client as location_client:
            # Llamar al servicio de ubicación para crear la rampa
            logger.info(f"📞 Llamando al location_service para crear rampa")
            
            result = await location_client.post(
                f"{config.API_PREFIX}/ramps",
                data=create_request.dict(),
                headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
            )
            
            logger.info(f"✅ Rampa creada exitosamente")
            
            # Convertir la respuesta a RampResponse
            return RampResponse(**result) 