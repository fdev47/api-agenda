"""
Use case para obtener sucursal por ID desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.branch.dto.responses.branch_responses import BranchResponse

class GetBranchUseCase:
    """Use case para obtener sucursal por ID usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, branch_id: int, access_token: str = "") -> Optional[BranchResponse]:
        """
        Obtener sucursal por ID desde el location_service
        
        Args:
            branch_id: ID de la sucursal a obtener
            access_token: Token de autorización
            
        Returns:
            Optional[BranchResponse]: Sucursal encontrada o None si no existe
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/branches/{branch_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/branches/{branch_id}",
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response:
                    return BranchResponse(**response)

                return None

        except Exception as e:
            print(f"Error obteniendo sucursal {branch_id}: {e}")
            return None 