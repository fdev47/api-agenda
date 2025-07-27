"""
Caso de uso para crear una dirección
"""
from uuid import uuid4
from ...domain.interfaces.address_repository import AddressRepository
from ...domain.entities.address import Address
from ...domain.dto.requests.address_requests import CreateAddressRequest
from ...domain.dto.responses.address_responses import AddressCreatedResponse
from ...domain.exceptions.user_exceptions import UserException


class CreateAddressUseCase:
    """Caso de uso para crear una dirección"""
    
    def __init__(self, address_repository: AddressRepository):
        self.address_repository = address_repository
    
    async def execute(self, request: CreateAddressRequest) -> AddressCreatedResponse:
        """Ejecutar el caso de uso"""
        try:
            # Crear entidad Address
            address = Address(
                id=uuid4(),
                street=request.street,
                city_id=request.city_id,
                state_id=request.state_id,
                country_id=request.country_id,
                postal_code=request.postal_code,
                additional_info=request.additional_info
            )
            
            # Guardar en el repositorio
            created_address = await self.address_repository.create(address)
            
            return AddressCreatedResponse(
                id=created_address.id,
                message="Dirección creada exitosamente"
            )
            
        except Exception as e:
            raise UserException(f"Error inesperado al crear dirección: {str(e)}") 