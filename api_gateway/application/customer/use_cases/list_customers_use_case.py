"""
Use case para listar customers desde API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ..utils.error_handler import handle_auth_service_error
from ....domain.customer.dto.responses.customer_responses import CustomerListResponse

class ListCustomersUseCase:
    """Use case para listar customers desde User Service"""
    
    def __init__(self):
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, page: int = 1, size: int = 100, access_token: str = None) -> CustomerListResponse:
        """Ejecutar el use case"""
        try:
            # Crear cliente para User Service
            async with APIClient(self.user_service_url, access_token) as client:
                # Obtener lista de customers del User Service
                response = await client.get(f"{config.API_PREFIX}/customers/", params={"page": page, "size": size})
                
                # Convertir a DTO
                return CustomerListResponse(**response)
                
        except Exception as e:
            handle_auth_service_error(e)