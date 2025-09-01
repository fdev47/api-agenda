"""
Use case para actualizar un sector desde el API Gateway
"""
from commons.api_client import APIClient
from commons.config import config
from ....domain.sector.dto.requests.sector_requests import UpdateSectorRequest
from ....domain.sector.dto.responses.sector_responses import SectorUpdatedResponse
from typing import Optional

class UpdateSectorUseCase:
    """Use case para actualizar un sector usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, sector_id: int, request: UpdateSectorRequest, access_token: str = "") -> Optional[SectorUpdatedResponse]:
        """
        Actualizar un sector desde el location_service
        
        Args:
            sector_id: ID del sector a actualizar
            request: Datos del sector a actualizar
            access_token: Token de autorización
            
        Returns:
            Optional[SectorUpdatedResponse]: Sector actualizado o None
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/sectors/{sector_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.put(
                    f"{config.API_PREFIX}/sectors/{sector_id}",
                    json=request.dict(exclude_unset=True),
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response:
                    return SectorUpdatedResponse(**response)

                return None

        except Exception as e:
            print(f"Error actualizando sector {sector_id}: {e}")
            return None
