"""
Caso de uso para obtener el customer actual
"""
from ...domain.interfaces.customer_repository import CustomerRepository
from ...domain.dto.responses.customer_responses import CustomerResponse
from ...domain.exceptions.user_exceptions import UserException, UserNotFoundException

class GetCurrentCustomerUseCase:
    """Caso de uso para obtener el customer actual"""

    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def execute(self, auth_uid: str) -> CustomerResponse:
        """Ejecutar el caso de uso"""
        try:
            customer = await self.customer_repository.get_by_auth_uid(auth_uid)
            
            if not customer:
                raise UserNotFoundException(f"Customer con auth_uid {auth_uid} no encontrado")
            
            return CustomerResponse.model_validate(customer)
            
        except UserException:
            raise
        except Exception as e:
            raise UserException(f"Error inesperado al obtener customer actual: {str(e)}") 