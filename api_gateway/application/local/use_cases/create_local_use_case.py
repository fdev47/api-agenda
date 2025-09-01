"""
Use case para crear local desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.local.dto.requests.local_requests import CreateLocalRequest
from ....domain.local.dto.responses.local_responses import LocalCreatedResponse

class CreateLocalUseCase:
    """Use case para crear local usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, request: CreateLocalRequest, access_token: str = "") -> LocalCreatedResponse:
        """
        Crear local desde el location_service
        
        Args:
            request: Datos del local a crear
            access_token: Token de autorización
            
        Returns:
            LocalCreatedResponse: Respuesta con el ID del local creado
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/locals/")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.post(
                    f"{config.API_PREFIX}/locals/",
                    data=request.dict(),
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "id" in response:
                    return LocalCreatedResponse(
                        id=response["id"],
                        message="Local creado exitosamente"
                    )

                raise Exception("Error al crear local: respuesta inválida")

        except Exception as e:
            print(f"Error creando local: {e}")
            raise 