"""
Use case para listar perfiles desde el API Gateway
"""
from typing import List
from commons.api_client import APIClient
from commons.config import config
from ....domain.dto.responses.profile_responses import ProfileResponse

class ListProfilesUseCase:
    """Use case para listar perfiles usando user_service"""
    
    def __init__(self):
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, skip: int = 0, limit: int = 100, access_token: str = "") -> List[ProfileResponse]:
        """
        Listar perfiles desde el user_service
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros
            access_token: Token de acceso para autenticación
            
        Returns:
            List[ProfileResponse]: Lista de perfiles
        """
        try:
            async with APIClient(self.user_service_url, access_token) as client:
                response = await client.get(
                    f"{config.API_PREFIX}/profiles/",
                    params={"skip": skip, "limit": limit}
                )
                
                if response and "profiles" in response:
                    profiles = response["profiles"]
                    return [ProfileResponse(**profile) for profile in profiles]
                
                return []
                
        except Exception as e:
            # En caso de error, retornar lista vacía
            print(f"Error obteniendo perfiles: {e}")
            return [] 