"""
Use case para obtener cliente por ID
"""
from uuid import UUID
from ...domain.interfaces.customer_repository import CustomerRepository
from ...domain.dto.responses.customer_responses import CustomerResponse
from ...domain.exceptions.user_exceptions import UserNotFoundException


class GetCustomerByIdUseCase:
    """Use case para obtener cliente por ID"""
    
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository
    
    async def execute(self, customer_id: UUID) -> CustomerResponse:
        """Ejecutar el use case"""
        customer = await self._customer_repository.get_by_id(customer_id)
        
        if not customer:
            raise UserNotFoundException(f"customer_id: {customer_id}")
        
        return CustomerResponse.model_validate(customer) 