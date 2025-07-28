"""
Use case para listar sucursales desde el API Gateway
"""
from typing import List, Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.location.dto.responses.location_responses import BranchResponse

class ListBranchesUseCase:
    """Use case para listar sucursales usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, skip: int = 0, limit: int = 100, name: Optional[str] = None, code: Optional[str] = None, local_id: Optional[int] = None, country_id: Optional[int] = None, state_id: Optional[int] = None, city_id: Optional[int] = None, is_active: Optional[bool] = None, access_token: str = "") -> List[BranchResponse]:
        """
        Listar sucursales desde el location_service
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros
            name: Filtrar por nombre
            code: Filtrar por código
            local_id: Filtrar por local
            country_id: Filtrar por país
            state_id: Filtrar por estado
            city_id: Filtrar por ciudad
            is_active: Filtrar por estado activo
            access_token: Token de autorización
            
        Returns:
            List[BranchResponse]: Lista de sucursales
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/branches/")
            
            # Construir parámetros de filtro
            params = {"skip": skip, "limit": limit}
            if name:
                params["name"] = name
            if code:
                params["code"] = code
            if local_id:
                params["local_id"] = local_id
            if country_id:
                params["country_id"] = country_id
            if state_id:
                params["state_id"] = state_id
            if city_id:
                params["city_id"] = city_id
            if is_active is not None:
                params["is_active"] = is_active
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/branches/",
                    params=params,
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "branches" in response:
                    branches = response["branches"]
                    return [BranchResponse(**branch) for branch in branches]

                return []

        except Exception as e:
            print(f"Error obteniendo sucursales: {e}")
            return [] 