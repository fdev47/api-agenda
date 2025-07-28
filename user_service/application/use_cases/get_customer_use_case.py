"""
Caso de uso para obtener un customer por ID
"""
from uuid import UUID
from ...domain.interfaces.customer_repository import CustomerRepository
from ...domain.dto.responses.customer_responses import CustomerResponse
from ...domain.exceptions.user_exceptions import UserException, UserNotFoundException

class GetCustomerUseCase:
    """Caso de uso para obtener un customer por ID"""

    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def execute(self, customer_id: UUID) -> CustomerResponse:
        """Ejecutar el caso de uso"""
        try:
            customer = await self.customer_repository.get_by_id(customer_id)
            if not customer:
                raise UserNotFoundException(f"Customer con ID {customer_id} no encontrado")
            
            return CustomerResponse.model_validate(customer)
            
        except UserException:
            raise
        except Exception as e:
            raise UserException(f"Error inesperado al obtener customer: {str(e)}") 