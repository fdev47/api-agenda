"""
Use case para listar sectores desde el API Gateway
"""
from typing import List, Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.sector.dto.responses.sector_responses import SectorResponse

class ListSectorsUseCase:
    """Use case para listar sectores usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, skip: int = 0, limit: int = 100, name: Optional[str] = None, branch_id: Optional[int] = None, sector_type_id: Optional[int] = None, is_active: Optional[bool] = None, access_token: str = "") -> List[SectorResponse]:
        """
        Listar sectores desde el location_service
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros
            name: Filtrar por nombre
            branch_id: Filtrar por sucursal
            sector_type_id: Filtrar por tipo de sector
            is_active: Filtrar por estado activo
            access_token: Token de autorización
            
        Returns:
            List[SectorResponse]: Lista de sectores
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/sectors/")
            
            # Construir parámetros de filtro
            params = {"skip": skip, "limit": limit}
            if name:
                params["name"] = name
            if branch_id:
                params["branch_id"] = branch_id
            if sector_type_id:
                params["sector_type_id"] = sector_type_id
            if is_active is not None:
                params["is_active"] = str(is_active).lower()  # Convertir boolean a string
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/sectors/",
                    params=params,
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "sectors" in response:
                    sectors = response["sectors"]
                    return [SectorResponse(**sector) for sector in sectors]

                return []

        except Exception as e:
            print(f"Error obteniendo sectores: {e}")
            return []
