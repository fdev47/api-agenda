"""
Use case para listar unidades de medida desde el API Gateway
"""
from typing import List, Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.measurement_unit.dto.responses.measurement_unit_responses import MeasurementUnitResponse

class ListMeasurementUnitsUseCase:
    """Use case para listar unidades de medida usando location_service"""
    
    def __init__(self):
        self.location_service_url = config.LOCATION_SERVICE_URL
    
    async def execute(self, skip: int = 0, limit: int = 100, name: Optional[str] = None, code: Optional[str] = None, is_active: Optional[bool] = None) -> List[MeasurementUnitResponse]:
        """
        Listar unidades de medida desde el location_service
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros
            name: Filtrar por nombre
            code: Filtrar por código
            is_active: Filtrar por estado activo
            
        Returns:
            List[MeasurementUnitResponse]: Lista de unidades de medida
        """
        try:
            print(f"🔍 DEBUG: Conectando a {self.location_service_url}")
            print(f"🔍 DEBUG: URL completa: {self.location_service_url}{config.API_PREFIX}/measurement-units/")
            
            # Construir parámetros de filtro
            params = {"skip": skip, "limit": limit}
            if name:
                params["name"] = name
            if code:
                params["code"] = code
            if is_active is not None:
                params["is_active"] = str(is_active).lower()  # Convertir boolean a string
            
            async with APIClient(self.location_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/measurement-units/",
                    params=params
                )
                
                print(f"🔍 DEBUG: Response recibida: {response}")
                
                if response and "items" in response:
                    measurement_units = response["items"]
                    return [MeasurementUnitResponse(**unit) for unit in measurement_units]
                
                return []
                
        except Exception as e:
            # En caso de error, retornar lista vacía
            print(f"Error obteniendo unidades de medida: {e}")
            return [] 