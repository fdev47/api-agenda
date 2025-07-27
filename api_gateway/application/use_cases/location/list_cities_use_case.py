"""
Use case para listar ciudades desde el API Gateway
"""
from typing import List, Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.dto.responses.location_responses import CityResponse

class ListCitiesUseCase:
    """Use case para listar ciudades usando location_service"""
    
    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL
    
    async def execute(self, skip: int = 0, limit: int = 100, state_id: Optional[str] = None) -> List[CityResponse]:
        """
        Listar ciudades desde el location_service
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros
            state_id: ID del estado para filtrar ciudades
            
        Returns:
            List[CityResponse]: Lista de ciudades
        """
        try:
            params = {"skip": skip, "limit": limit}
            if state_id:
                params["state_id"] = state_id
                
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/cities/",
                    params=params
                )
                
                if response and "cities" in response:
                    cities = response["cities"]
                    return [CityResponse(**city) for city in cities]
                
                return []
                
        except Exception as e:
            # En caso de error, retornar lista vacía
            print(f"Error obteniendo ciudades: {e}")
            return [] 