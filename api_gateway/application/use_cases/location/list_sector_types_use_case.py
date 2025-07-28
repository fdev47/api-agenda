"""
Use case para listar tipos de sector desde el API Gateway
"""
from typing import List, Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.dto.responses.location_responses import SectorTypeResponse

class ListSectorTypesUseCase:
    """Use case para listar tipos de sector usando location_service"""
    
    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL
    
    async def execute(self, skip: int = 0, limit: int = 100, name: Optional[str] = None, code: Optional[str] = None, is_active: Optional[bool] = None) -> List[SectorTypeResponse]:
        """
        Listar tipos de sector desde el location_service
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros
            name: Filtrar por nombre
            code: Filtrar por código
            is_active: Filtrar por estado activo
            
        Returns:
            List[SectorTypeResponse]: Lista de tipos de sector
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/sector-types/")
            
            # Construir parámetros de filtro
            params = {"skip": skip, "limit": limit}
            if name:
                params["name"] = name
            if code:
                params["code"] = code
            if is_active is not None:
                params["is_active"] = is_active
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/sector-types/",
                    params=params
                )
                
                print(f"🔍 DEBUG: Response recibida: {response}")
                
                if response and "sector_types" in response:
                    sector_types = response["sector_types"]
                    return [SectorTypeResponse(**sector_type) for sector_type in sector_types]
                
                return []
                
        except Exception as e:
            # En caso de error, retornar lista vacía
            print(f"Error obteniendo tipos de sector: {e}")
            return [] 