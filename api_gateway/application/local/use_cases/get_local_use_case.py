"""
Use case para obtener local por ID desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.local.dto.responses.local_responses import LocalResponse

class GetLocalUseCase:
    """Use case para obtener local por ID usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, local_id: int, access_token: str = "") -> Optional[LocalResponse]:
        """
        Obtener local por ID desde el location_service
        
        Args:
            local_id: ID del local a obtener
            access_token: Token de autorización
            
        Returns:
            Optional[LocalResponse]: Local encontrado o None si no existe
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/locals/{local_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/locals/{local_id}",
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response:
                    return LocalResponse(**response)

                return None

        except Exception as e:
            print(f"Error obteniendo local {local_id}: {e}")
            return None 