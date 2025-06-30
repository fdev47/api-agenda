"""
Use case para obtener cliente por auth_uid
"""
from uuid import UUID
from ...domain.interfaces.customer_repository import CustomerRepository
from ...domain.dto.responses.customer_responses import CustomerResponse
from ...domain.exceptions.user_exceptions import UserNotFoundException


class GetCustomerByAuthUidUseCase:
    """Use case para obtener cliente por auth_uid"""
    
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository
    
    async def execute(self, auth_uid: str) -> CustomerResponse:
        """Ejecutar el use case"""
        customer = await self._customer_repository.get_by_auth_uid(auth_uid)
        
        if not customer:
            raise UserNotFoundException(f"Cliente no encontrado: auth_uid {auth_uid}")
        
        return CustomerResponse.model_validate(customer) 