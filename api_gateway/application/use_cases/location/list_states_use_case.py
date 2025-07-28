"""
Use case para listar estados desde el API Gateway
"""
from typing import List, Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.location.dto.responses.location_responses import StateResponse

class ListStatesUseCase:
    """Use case para listar estados usando location_service"""
    
    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL
    
    async def execute(self, skip: int = 0, limit: int = 100, country_id: Optional[str] = None) -> List[StateResponse]:
        """
        Listar estados desde el location_service
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros
            country_id: ID del país para filtrar estados
            
        Returns:
            List[StateResponse]: Lista de estados
        """
        try:
            params = {"skip": skip, "limit": limit}
            if country_id:
                params["country_id"] = country_id
                
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/states/",
                    params=params
                )
                
                if response and "states" in response:
                    states = response["states"]
                    return [StateResponse(**state) for state in states]
                
                return []
                
        except Exception as e:
            # En caso de error, retornar lista vacía
            print(f"Error obteniendo estados: {e}")
            return [] 