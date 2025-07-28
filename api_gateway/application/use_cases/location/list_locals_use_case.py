"""
Use case para listar locales desde el API Gateway
"""
from typing import List, Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.dto.responses.location_responses import LocalResponse

class ListLocalsUseCase:
    """Use case para listar locales usando location_service"""

    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL

    async def execute(self, skip: int = 0, limit: int = 100, name: Optional[str] = None, code: Optional[str] = None, is_active: Optional[bool] = None, access_token: str = "") -> List[LocalResponse]:
        """
        Listar locales desde el location_service
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros
            name: Filtrar por nombre
            code: Filtrar por código
            is_active: Filtrar por estado activo
            access_token: Token de autorización
            
        Returns:
            List[LocalResponse]: Lista de locales
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/locals/")
            
            # Construir parámetros de filtro
            params = {"skip": skip, "limit": limit}
            if name:
                params["name"] = name
            if code:
                params["code"] = code
            if is_active is not None:
                params["is_active"] = is_active
            
            # Headers con autorización
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/locals/",
                    params=params,
                    headers=headers
                )

                print(f"🔍 DEBUG: Response recibida: {response}")

                if response and "locals" in response:
                    locals = response["locals"]
                    return [LocalResponse(**local) for local in locals]

                return []

        except Exception as e:
            print(f"Error obteniendo locales: {e}")
            return [] 