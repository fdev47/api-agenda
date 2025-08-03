"""
Use case para actualizar unidad de medida desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.measurement_unit.dto.requests.measurement_unit_requests import UpdateMeasurementUnitRequest
from ....domain.measurement_unit.dto.responses.measurement_unit_responses import MeasurementUnitUpdatedResponse

class UpdateMeasurementUnitUseCase:
    """Use case para actualizar unidad de medida usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, measurement_unit_id: int, request: UpdateMeasurementUnitRequest, access_token: str = "") -> Optional[MeasurementUnitUpdatedResponse]:
        """
        Actualizar unidad de medida desde el location_service
        
        Args:
            measurement_unit_id: ID de la unidad de medida a actualizar
            request: Datos de la unidad de medida a actualizar
            access_token: Token de autorización
            
        Returns:
            Optional[MeasurementUnitUpdatedResponse]: Respuesta con los datos de la unidad de medida actualizada o None si no existe
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/measurement-units/{measurement_unit_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.put(
                    f"{config.API_PREFIX}/measurement-units/{measurement_unit_id}",
                    json=request.dict(exclude_none=True),
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "id" in response:
                    return MeasurementUnitUpdatedResponse(
                        id=response["id"],
                        name=response["name"],
                        code=response["code"],
                        description=response.get("description"),
                        is_active=response["is_active"],
                        updated_at=response["updated_at"],
                        message="Unidad de medida actualizada exitosamente"
                    )

                return None

        except Exception as e:
            print(f"Error actualizando unidad de medida {measurement_unit_id}: {e}")
            return None 