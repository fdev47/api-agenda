"""
Use case para obtener customer por username desde API Gateway
"""
from typing import Optional, Dict, Any
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_not_found_error, raise_internal_error
from ....domain.customer.dto.responses.customer_responses import CustomerResponse
from ..utils.error_handler import handle_auth_service_error

class GetCustomerByUsernameUseCase:
    """Use case para obtener customer por username desde User Service"""
    
    def __init__(self):
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, username: str, access_token: str) -> CustomerResponse:
        """Ejecutar el use case"""
        try:
            # Crear cliente para User Service con token
            async with APIClient(self.user_service_url, access_token) as client:
                # Obtener customer del User Service por username
                response = await client.get(f"{config.API_PREFIX}/customers/by-username/{username}")
                
                # Convertir a DTO
                return CustomerResponse(**response)
                
        except Exception as e:
            handle_auth_service_error(e)
