"""
Use case para crear unidad de medida desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.measurement_unit.dto.requests.measurement_unit_requests import CreateMeasurementUnitRequest
from ....domain.measurement_unit.dto.responses.measurement_unit_responses import MeasurementUnitCreatedResponse

class CreateMeasurementUnitUseCase:
    """Use case para crear unidad de medida usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, request: CreateMeasurementUnitRequest, access_token: str = "") -> MeasurementUnitCreatedResponse:
        """
        Crear unidad de medida desde el location_service
        
        Args:
            request: Datos de la unidad de medida a crear
            access_token: Token de autorización
            
        Returns:
            MeasurementUnitCreatedResponse: Respuesta con los datos de la unidad de medida creada
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/measurement-units/")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.post(
                    f"{config.API_PREFIX}/measurement-units/",
                    json=request.dict(),
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "id" in response:
                    return MeasurementUnitCreatedResponse(
                        id=response["id"],
                        name=response["name"],
                        code=response["code"],
                        description=response.get("description"),
                        is_active=response["is_active"],
                        created_at=response["created_at"],
                        message="Unidad de medida creada exitosamente"
                    )

                raise Exception("Error al crear unidad de medida: respuesta inválida")

        except Exception as e:
            print(f"Error creando unidad de medida: {e}")
            raise 