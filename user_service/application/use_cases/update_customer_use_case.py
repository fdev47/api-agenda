"""
Caso de uso para actualizar un customer
"""
from uuid import UUID
from ...domain.interfaces.customer_repository import CustomerRepository
from ...domain.interfaces.address_repository import AddressRepository
from ...domain.entities.customer import Customer
from ...domain.entities.address import Address
from ...domain.dto.requests.customer_requests import UpdateCustomerRequest
from ...domain.dto.responses.customer_responses import CustomerUpdatedResponse, CustomerResponse
from ...domain.exceptions.user_exceptions import (
    UserException, 
    UserNotFoundException,
    CustomerAuthUidAlreadyExistsException,
    CustomerRucAlreadyExistsException,
    CustomerEmailAlreadyExistsException,
    CustomerUsernameAlreadyExistsException
)

class UpdateCustomerUseCase:
    """Caso de uso para actualizar un customer"""

    def __init__(self, customer_repository: CustomerRepository, address_repository: AddressRepository):
        self.customer_repository = customer_repository
        self.address_repository = address_repository

    async def execute(self, customer_id: UUID, request: UpdateCustomerRequest) -> CustomerUpdatedResponse:
        """Ejecutar el caso de uso"""
        try:
            # 1. Verificar que el customer existe
            existing_customer = await self.customer_repository.get_by_id(customer_id)
            if not existing_customer:
                raise UserNotFoundException(f"Customer con ID {customer_id} no encontrado")
            
            # 2. Actualizar dirección si se proporciona
            if request.address:
                # Obtener la dirección actual del customer
                current_address = await self.address_repository.get_by_id(existing_customer.address_id)
                if current_address:
                    # Actualizar la dirección existente
                    current_address.street = request.address.street
                    current_address.city_id = request.address.city_id
                    current_address.state_id = request.address.state_id
                    current_address.country_id = request.address.country_id
                    current_address.postal_code = request.address.postal_code
                    current_address.additional_info = request.address.additional_info
                    
                    await self.address_repository.update(current_address)
                    print(f"✅ Dirección actualizada: {current_address.id}")
            
            # 3. Actualizar customer
            update_data = request.model_dump(exclude_unset=True, exclude={'address'})
            if update_data:
                updated_customer = await self.customer_repository.update(customer_id, update_data)
            else:
                updated_customer = existing_customer
            
            return CustomerUpdatedResponse(
                customer=CustomerResponse.model_validate(updated_customer),
                message="Customer actualizado exitosamente"
            )
        
        except (
            CustomerAuthUidAlreadyExistsException,
            CustomerRucAlreadyExistsException,
            CustomerEmailAlreadyExistsException,
            CustomerUsernameAlreadyExistsException
        ):
            # Re-lanzar las excepciones de duplicidad para que sean manejadas por la capa de API
            raise
        except UserException:
            raise
        except Exception as e:
            raise UserException(f"Error inesperado al actualizar customer: {str(e)}") 