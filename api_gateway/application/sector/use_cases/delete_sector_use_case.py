"""
Use case para eliminar un sector desde el API Gateway
"""
from commons.api_client import APIClient
from commons.config import config
from ....domain.sector.dto.responses.sector_responses import SectorDeletedResponse
from typing import Optional

class DeleteSectorUseCase:
    """Use case para eliminar un sector usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, sector_id: int, access_token: str = "") -> Optional[SectorDeletedResponse]:
        """
        Eliminar un sector desde el location_service
        
        Args:
            sector_id: ID del sector a eliminar
            access_token: Token de autorización
            
        Returns:
            Optional[SectorDeletedResponse]: Sector eliminado o None
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/sectors/{sector_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.delete(
                    f"{config.API_PREFIX}/sectors/{sector_id}",
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response:
                    return SectorDeletedResponse(**response)

                return None

        except Exception as e:
            print(f"Error eliminando sector {sector_id}: {e}")
            return None
