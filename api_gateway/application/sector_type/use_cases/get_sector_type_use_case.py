"""
Use case para obtener tipo de sector por ID desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.sector_type.dto.responses.sector_type_responses import SectorTypeResponse

class GetSectorTypeUseCase:
    """Use case para obtener tipo de sector por ID usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, sector_type_id: int, access_token: str = "") -> Optional[SectorTypeResponse]:
        """
        Obtener tipo de sector por ID desde el location_service
        
        Args:
            sector_type_id: ID del tipo de sector a obtener
            access_token: Token de autorización
            
        Returns:
            Optional[SectorTypeResponse]: Tipo de sector encontrado o None si no existe
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/sector-types/{sector_type_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/sector-types/{sector_type_id}",
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response:
                    return SectorTypeResponse(**response)

                return None

        except Exception as e:
            print(f"Error obteniendo tipo de sector {sector_type_id}: {e}")
            return None 