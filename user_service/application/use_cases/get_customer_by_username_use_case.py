"""
Use case para obtener customer por username
"""
from ...domain.interfaces.customer_repository import CustomerRepository
from ...domain.dto.responses.customer_responses import CustomerResponse
from ...domain.exceptions.user_exceptions import UserNotFoundException


class GetCustomerByUsernameUseCase:
    """Use case para obtener customer por username"""
    
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository
    
    async def execute(self, username: str) -> CustomerResponse:
        """Ejecutar el use case"""
        customer = await self._customer_repository.get_by_username(username)
        
        if not customer:
            raise UserNotFoundException(f"username: {username}")
        
        return CustomerResponse.model_validate(customer)
