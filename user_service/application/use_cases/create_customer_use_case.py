"""
Caso de uso para crear un customer
"""
from uuid import uuid4
from ...domain.interfaces.customer_repository import CustomerRepository
from ...domain.interfaces.address_repository import AddressRepository
from ...domain.entities.customer import Customer
from ...domain.entities.address import Address
from ...domain.dto.requests.customer_requests import CreateCustomerRequest
from ...domain.dto.responses.customer_responses import CustomerResponse
from ...domain.exceptions.user_exceptions import (
    UserException,
    CustomerAuthUidAlreadyExistsException,
    CustomerRucAlreadyExistsException,
    CustomerEmailAlreadyExistsException,
    CustomerUsernameAlreadyExistsException
)

class CreateCustomerUseCase:
    """Caso de uso para crear un customer"""

    def __init__(self, customer_repository: CustomerRepository, address_repository: AddressRepository):
        self.customer_repository = customer_repository
        self.address_repository = address_repository

    async def execute(self, request: CreateCustomerRequest) -> CustomerResponse:
        """Ejecutar el caso de uso"""
        try:
            # 1. Crear la dirección
            address = Address(
                id=uuid4(),
                street=request.address.street,
                city_id=request.address.city_id,
                state_id=request.address.state_id,
                country_id=request.address.country_id,
                postal_code=request.address.postal_code,
                additional_info=request.address.additional_info
            )
            
            created_address = await self.address_repository.create(address)
            print(f"✅ Dirección creada: {created_address.id}")
            
            # 2. Crear el customer
            customer = Customer(
                id=uuid4(),
                auth_uid=request.auth_uid,
                ruc=request.ruc,
                company_name=request.company_name,
                email=request.email,
                username=request.username,
                phone=request.phone,
                cellphone_number=request.cellphone_number,
                cellphone_country_code=request.cellphone_country_code,
                address_id=created_address.id,
                is_active=request.is_active
            )
            
            created_customer = await self.customer_repository.create(customer)
            
            # 3. Retornar CustomerResponse completo
            return CustomerResponse.model_validate(created_customer)

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
            raise UserException(f"Error inesperado al crear customer: {str(e)}") 