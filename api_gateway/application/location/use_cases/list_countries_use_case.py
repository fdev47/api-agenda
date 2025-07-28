"""
Use case para listar países desde el API Gateway
"""
from typing import List
from commons.api_client import APIClient
from commons.config import config
from ....domain.location.dto.responses.location_responses import CountryResponse

class ListCountriesUseCase:
    """Use case para listar países usando location_service"""
    
    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL
    
    async def execute(self, skip: int = 0, limit: int = 100) -> List[CountryResponse]:
        """
        Listar países desde el location_service
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros
            
        Returns:
            List[CountryResponse]: Lista de países
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/countries/")
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/countries/",
                    params={"skip": skip, "limit": limit}
                )
                
                print(f"🔍 DEBUG: Response recibida: {response}")
                
                if response and "countries" in response:
                    countries = response["countries"]
                    return [CountryResponse(**country) for country in countries]
                
                return []
                
        except Exception as e:
            # En caso de error, retornar lista vacía
            print(f"Error obteniendo países: {e}")
            return [] 