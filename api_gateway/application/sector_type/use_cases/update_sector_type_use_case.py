"""
Use case para actualizar tipo de sector desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.sector_type.dto.requests.sector_type_requests import UpdateSectorTypeRequest
from ....domain.sector_type.dto.responses.sector_type_responses import SectorTypeUpdatedResponse

class UpdateSectorTypeUseCase:
    """Use case para actualizar tipo de sector usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, sector_type_id: int, request: UpdateSectorTypeRequest, access_token: str = "") -> Optional[SectorTypeUpdatedResponse]:
        """
        Actualizar tipo de sector desde el location_service
        
        Args:
            sector_type_id: ID del tipo de sector a actualizar
            request: Datos del tipo de sector a actualizar
            access_token: Token de autorización
            
        Returns:
            Optional[SectorTypeUpdatedResponse]: Respuesta con los datos del tipo de sector actualizado o None si no existe
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/sector-types/{sector_type_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.put(
                    f"{config.API_PREFIX}/sector-types/{sector_type_id}",
                    json=request.dict(exclude_none=True),
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "id" in response:
                    return SectorTypeUpdatedResponse(
                        id=response["id"],
                        name=response["name"],
                        code=response["code"],
                        measurement_unit=response["measurement_unit"],
                        message="Tipo de sector actualizado exitosamente"
                    )

                return None

        except Exception as e:
            print(f"Error actualizando tipo de sector {sector_type_id}: {e}")
            return None 