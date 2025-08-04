"""
Caso de uso para listar rampas en API Gateway
"""
import logging
from commons.api_client import HTTPError, APIClient
from commons.config import config
from ....domain.ramp.dto.requests.ramp_filter_request import RampFilterRequest
from ....domain.ramp.dto.responses.ramp_list_response import RampListResponse

logger = logging.getLogger(__name__)


class ListRampsUseCase:
    """Caso de uso para listar rampas"""
    
    def __init__(self):
        self.location_client = APIClient(base_url=config.LOCATION_SERVICE_URL)
    
    async def execute(self, filter_request: RampFilterRequest, access_token: str = "") -> RampListResponse:
        """
        Ejecutar el caso de uso para listar rampas
        
        Args:
            filter_request: Filtros para la búsqueda
            access_token: Token de acceso para autenticación
            
        Returns:
            RampListResponse: Lista de rampas
            
        Raises:
            HTTPError: Si hay errores en el servicio de ubicación
        """
        logger.info(f"🚀 Ejecutando ListRampsUseCase")
        
        # Usar context manager para el cliente HTTP
        async with self.location_client as location_client:
            # Construir parámetros de query
            params = {}
            if filter_request.branch_id is not None:
                params["branch_id"] = filter_request.branch_id
            if filter_request.name is not None:
                params["name"] = filter_request.name
            if filter_request.is_available is not None:
                params["is_available"] = filter_request.is_available
            params["skip"] = filter_request.skip
            params["limit"] = filter_request.limit
            if filter_request.sort_by is not None:
                params["sort_by"] = filter_request.sort_by
            if filter_request.sort_order is not None:
                params["sort_order"] = filter_request.sort_order
            
            # Llamar al servicio de ubicación para listar rampas
            logger.info(f"📞 Llamando al location_service para listar rampas")
            
            result = await location_client.get(
                f"{config.API_PREFIX}/ramps",
                params=params,
                headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
            )
            
            logger.info(f"✅ Rampas listadas exitosamente")
            
            # Convertir la respuesta a RampListResponse
            return RampListResponse(**result) 