"""
Use case para eliminar sucursal desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.branch.dto.responses.branch_responses import BranchDeletedResponse

class DeleteBranchUseCase:
    """Use case para eliminar sucursal usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, branch_id: int, access_token: str = "") -> Optional[BranchDeletedResponse]:
        """
        Eliminar sucursal desde el location_service
        
        Args:
            branch_id: ID de la sucursal a eliminar
            access_token: Token de autorización
            
        Returns:
            Optional[BranchDeletedResponse]: Respuesta con el ID de la sucursal eliminada o None si no existe
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/branches/{branch_id}")
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.delete(
                    f"{config.API_PREFIX}/branches/{branch_id}",
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "success" in response and response["success"]:
                    return BranchDeletedResponse(
                        id=branch_id,
                        message=f"Sucursal {branch_id} eliminada exitosamente"
                    )

                return None

        except Exception as e:
            print(f"Error eliminando sucursal {branch_id}: {e}")
            return None 