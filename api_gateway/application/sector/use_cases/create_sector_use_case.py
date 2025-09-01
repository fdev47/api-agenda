"""
Use case para crear un sector desde el API Gateway
"""
from commons.api_client import APIClient
from commons.config import config
from ....domain.sector.dto.requests.sector_requests import CreateSectorRequest
from ....domain.sector.dto.responses.sector_responses import SectorCreatedResponse
from typing import Optional

class CreateSectorUseCase:
    """Use case para crear un sector usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, request: CreateSectorRequest, access_token: str = "") -> Optional[SectorCreatedResponse]:
        """
        Crear un sector desde el location_service
        
        Args:
            request: Datos del sector a crear
            access_token: Token de autorización
            
        Returns:
            Optional[SectorCreatedResponse]: Sector creado o None
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/sectors/")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.post(
                    f"{config.API_PREFIX}/sectors/",
                    json=request.dict(),
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response:
                    return SectorCreatedResponse(**response)

                return None

        except Exception as e:
            print(f"Error creando sector: {e}")
            return None
