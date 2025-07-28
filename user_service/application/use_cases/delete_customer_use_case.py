"""
Caso de uso para eliminar un customer
"""
from uuid import UUID
from ...domain.interfaces.customer_repository import CustomerRepository
from ...domain.interfaces.address_repository import AddressRepository
from ...domain.dto.responses.customer_responses import CustomerDeletedResponse, CustomerResponse
from ...domain.exceptions.user_exceptions import UserException, UserNotFoundException

class DeleteCustomerUseCase:
    """Caso de uso para eliminar un customer"""

    def __init__(self, customer_repository: CustomerRepository, address_repository: AddressRepository):
        self.customer_repository = customer_repository
        self.address_repository = address_repository

    async def execute(self, customer_id: UUID) -> CustomerDeletedResponse:
        """Ejecutar el caso de uso"""
        try:
            # 1. Verificar que el customer existe
            customer = await self.customer_repository.get_by_id(customer_id)
            if not customer:
                raise UserNotFoundException(f"Customer con ID {customer_id} no encontrado")
            
            # 2. Eliminar la dirección asociada si existe
            if customer.address_id:
                try:
                    await self.address_repository.delete(customer.address_id)
                    print(f"✅ Dirección eliminada: {customer.address_id}")
                except Exception as e:
                    print(f"⚠️  Error eliminando dirección: {e}")
            
            # 3. Eliminar el customer
            await self.customer_repository.delete(customer_id)
            
            return CustomerDeletedResponse(
                customer=CustomerResponse.model_validate(customer),
                message="Customer eliminado exitosamente"
            )
            
        except UserException:
            raise
        except Exception as e:
            raise UserException(f"Error inesperado al eliminar customer: {str(e)}") 