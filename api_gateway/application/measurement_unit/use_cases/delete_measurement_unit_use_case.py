"""
Use case para eliminar unidad de medida desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.measurement_unit.dto.responses.measurement_unit_responses import MeasurementUnitDeletedResponse

class DeleteMeasurementUnitUseCase:
    """Use case para eliminar unidad de medida usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, measurement_unit_id: int, access_token: str = "") -> Optional[MeasurementUnitDeletedResponse]:
        """
        Eliminar unidad de medida desde el location_service
        
        Args:
            measurement_unit_id: ID de la unidad de medida a eliminar
            access_token: Token de autorización
            
        Returns:
            Optional[MeasurementUnitDeletedResponse]: Respuesta con el ID de la unidad de medida eliminada o None si no existe
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/measurement-units/{measurement_unit_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.delete(
                    f"{config.API_PREFIX}/measurement-units/{measurement_unit_id}",
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "success" in response and response["success"]:
                    return MeasurementUnitDeletedResponse(
                        id=measurement_unit_id,
                        message=f"Unidad de medida {measurement_unit_id} eliminada exitosamente"
                    )

                return None

        except Exception as e:
            print(f"Error eliminando unidad de medida {measurement_unit_id}: {e}")
            return None 