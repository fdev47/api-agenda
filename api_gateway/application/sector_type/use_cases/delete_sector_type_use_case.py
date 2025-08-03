"""
Use case para eliminar tipo de sector desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.sector_type.dto.responses.sector_type_responses import SectorTypeDeletedResponse

class DeleteSectorTypeUseCase:
    """Use case para eliminar tipo de sector usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, sector_type_id: int, access_token: str = "") -> Optional[SectorTypeDeletedResponse]:
        """
        Eliminar tipo de sector desde el location_service
        
        Args:
            sector_type_id: ID del tipo de sector a eliminar
            access_token: Token de autorización
            
        Returns:
            Optional[SectorTypeDeletedResponse]: Respuesta con el ID del tipo de sector eliminado o None si no existe
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/sector-types/{sector_type_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.delete(
                    f"{config.API_PREFIX}/sector-types/{sector_type_id}",
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "success" in response and response["success"]:
                    return SectorTypeDeletedResponse(
                        id=sector_type_id,
                        message=f"Tipo de sector {sector_type_id} eliminado exitosamente"
                    )

                return None

        except Exception as e:
            print(f"Error eliminando tipo de sector {sector_type_id}: {e}")
            return None 