"""
Use case para actualizar local desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.local.dto.requests.local_requests import UpdateLocalRequest
from ....domain.local.dto.responses.local_responses import LocalUpdatedResponse

class UpdateLocalUseCase:
    """Use case para actualizar local usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, local_id: int, request: UpdateLocalRequest, access_token: str = "") -> Optional[LocalUpdatedResponse]:
        """
        Actualizar local desde el location_service
        
        Args:
            local_id: ID del local a actualizar
            request: Datos del local a actualizar
            access_token: Token de autorización
            
        Returns:
            Optional[LocalUpdatedResponse]: Respuesta con el ID del local actualizado o None si no existe
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/locals/{local_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.put(
                    f"{config.API_PREFIX}/locals/{local_id}",
                    json=request.dict(exclude_none=True),
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "id" in response:
                    return LocalUpdatedResponse(
                        id=response["id"],
                        message="Local actualizado exitosamente"
                    )

                return None

        except Exception as e:
            print(f"Error actualizando local {local_id}: {e}")
            return None 