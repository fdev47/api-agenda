"""
Use case para eliminar customers usando auth_service y user_service
"""
from uuid import UUID
from commons.api_client import APIClient
from commons.config import config
from ..utils.error_handler import handle_auth_service_error
from ....domain.customer.dto.responses.customer_responses import CustomerDeletedResponse


class DeleteCustomerUseCase:
    """Use case para eliminar customers usando auth_service y user_service"""
    
    def __init__(self):
        self.auth_service_url = config.AUTH_SERVICE_URL
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, customer_id: UUID, access_token: str = None) -> CustomerDeletedResponse:
        """
        Eliminar customer de Firebase y de la base de datos
        
        Args:
            customer_id: ID del customer a eliminar
            access_token: Token de acceso para las llamadas a los servicios
            
        Returns:
            CustomerDeletedResponse: Confirmación de eliminación
        """
        try:
            # 1. Obtener información del customer para obtener el auth_uid
            customer_info = await self._get_customer_info(customer_id, access_token)
            auth_uid = customer_info["auth_uid"]
            
            # 2. Eliminar customer de la base de datos
            await self._delete_db_customer(customer_id, access_token)
            
            # 3. Eliminar usuario de Firebase
            await self._delete_firebase_user(auth_uid, access_token)
            
            return CustomerDeletedResponse(
                message="Customer eliminado exitosamente",
                customer_id=customer_id
            )
            
        except Exception as error:
            handle_auth_service_error(error)
    
    async def _get_customer_info(self, customer_id: UUID, access_token: str) -> dict:
        """Obtener información del customer para obtener el auth_uid"""
        async with APIClient(self.user_service_url, access_token) as client:
                response = await client.get(f"{config.API_PREFIX}/customers/{customer_id}")
                
                # Verificar si la respuesta tiene el formato esperado
                if isinstance(response, dict) and 'customer' in response:
                    # Si la respuesta tiene formato {'customer': {...}}
                    return response['customer']
                else:
                    # Si la respuesta es directa
                    return response
    
    async def _delete_db_customer(self, customer_id: UUID, access_token: str):
        """Eliminar customer de la base de datos"""
        async with APIClient(self.user_service_url, access_token) as client:
            await client.delete(f"{config.API_PREFIX}/customers/{customer_id}")
    
    async def _delete_firebase_user(self, auth_uid: str, access_token: str):
        """Eliminar usuario de Firebase"""
        async with APIClient(self.auth_service_url, access_token) as client:
            await client.delete(f"{config.API_PREFIX}/auth/users/{auth_uid}")
