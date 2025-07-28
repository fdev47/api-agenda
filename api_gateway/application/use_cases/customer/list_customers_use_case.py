"""
Use case para listar customers desde API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_internal_error
from ....domain.dto.responses.customer.customer_responses import CustomerListResponse


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
            raise_internal_error(
                message=f"Error obteniendo lista de customers: {str(e)}",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
            ) 