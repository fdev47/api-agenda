"""
Use case para crear sucursal desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.branch.dto.requests.branch_requests import CreateBranchRequest
from ....domain.branch.dto.responses.branch_responses import BranchCreatedResponse

class CreateBranchUseCase:
    """Use case para crear sucursal usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, request: CreateBranchRequest, access_token: str = "") -> BranchCreatedResponse:
        """
        Crear sucursal desde el location_service
        
        Args:
            request: Datos de la sucursal a crear
            access_token: Token de autorización
            
        Returns:
            BranchCreatedResponse: Respuesta con el ID de la sucursal creada
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/branches/")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.post(
                    f"{config.API_PREFIX}/branches/",
                    data=request.dict(),
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "id" in response:
                    return BranchCreatedResponse(
                        id=response["id"],
                        message="Sucursal creada exitosamente"
                    )

                raise Exception("Error al crear sucursal: respuesta inválida")

        except Exception as e:
            print(f"Error creando sucursal: {e}")
            raise 