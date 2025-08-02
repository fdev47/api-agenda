"""
Use case para actualizar sucursal desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.branch.dto.requests.branch_requests import UpdateBranchRequest
from ....domain.branch.dto.responses.branch_responses import BranchUpdatedResponse

class UpdateBranchUseCase:
    """Use case para actualizar sucursal usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, branch_id: int, request: UpdateBranchRequest, access_token: str = "") -> Optional[BranchUpdatedResponse]:
        """
        Actualizar sucursal desde el location_service
        
        Args:
            branch_id: ID de la sucursal a actualizar
            request: Datos de la sucursal a actualizar
            access_token: Token de autorización
            
        Returns:
            Optional[BranchUpdatedResponse]: Respuesta con el ID de la sucursal actualizada o None si no existe
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/branches/{branch_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.put(
                    f"{config.API_PREFIX}/branches/{branch_id}",
                    json=request.dict(exclude_none=True),
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "id" in response:
                    return BranchUpdatedResponse(
                        id=response["id"],
                        message="Sucursal actualizada exitosamente"
                    )

                return None

        except Exception as e:
            print(f"Error actualizando sucursal {branch_id}: {e}")
            return None 