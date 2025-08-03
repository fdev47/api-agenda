"""
Use case para crear tipo de sector desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.sector_type.dto.requests.sector_type_requests import CreateSectorTypeRequest
from ....domain.sector_type.dto.responses.sector_type_responses import SectorTypeCreatedResponse

class CreateSectorTypeUseCase:
    """Use case para crear tipo de sector usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, request: CreateSectorTypeRequest, access_token: str = "") -> SectorTypeCreatedResponse:
        """
        Crear tipo de sector desde el location_service
        
        Args:
            request: Datos del tipo de sector a crear
            access_token: Token de autorización
            
        Returns:
            SectorTypeCreatedResponse: Respuesta con los datos del tipo de sector creado
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/sector-types/")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.post(
                    f"{config.API_PREFIX}/sector-types/",
                    json=request.dict(),
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "id" in response:
                    return SectorTypeCreatedResponse(
                        id=response["id"],
                        name=response["name"],
                        code=response["code"],
                        measurement_unit=response["measurement_unit"],
                        message="Tipo de sector creado exitosamente"
                    )

                raise Exception("Error al crear tipo de sector: respuesta inválida")

        except Exception as e:
            print(f"Error creando tipo de sector: {e}")
            raise 