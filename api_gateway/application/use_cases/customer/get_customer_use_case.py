"""
Use case para obtener customer desde API Gateway
"""
from typing import Optional, Dict, Any
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_not_found_error, raise_internal_error
from ....domain.dto.responses.customer.customer_responses import CustomerResponse


class GetCustomerUseCase:
    """Use case para obtener customer desde User Service"""
    
    def __init__(self):
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, auth_uid: str, access_token: str) -> CustomerResponse:
        """Ejecutar el use case"""
        try:
            # Crear cliente para User Service con token
            async with APIClient(self.user_service_url, access_token) as client:
                # Obtener customer del User Service
                response = await client.get(f"{config.API_PREFIX}/customers/me")
                
                # Convertir a DTO
                return CustomerResponse(**response)
                
        except Exception as e:
            # Si el customer no existe, lanzar error específico
            if "404" in str(e) or "Customer no encontrado" in str(e):
                raise_not_found_error(
                    message="Customer no encontrado en el sistema",
                    error_code=ErrorCode.USER_NOT_FOUND.value
                )
            else:
                raise_internal_error(
                    message=f"Error obteniendo customer: {str(e)}",
                    error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
                ) 