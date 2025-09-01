"""
Use case para obtener un sector por ID desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.sector.dto.responses.sector_responses import SectorResponse

class GetSectorUseCase:
    """Use case para obtener un sector por ID usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, sector_id: int, access_token: str = "") -> Optional[SectorResponse]:
        """
        Obtener un sector por ID desde el location_service
        
        Args:
            sector_id: ID del sector a obtener
            access_token: Token de autorización
            
        Returns:
            Optional[SectorResponse]: Sector encontrado o None
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/sectors/{sector_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/sectors/{sector_id}",
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response:
                    return SectorResponse(**response)

                return None

        except Exception as e:
            print(f"Error obteniendo sector {sector_id}: {e}")
            return None
