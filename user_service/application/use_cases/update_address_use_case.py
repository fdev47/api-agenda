"""
Caso de uso para actualizar una dirección
"""
from uuid import UUID
from ...domain.interfaces.address_repository import AddressRepository
from ...domain.entities.address import Address
from ...domain.dto.requests.address_requests import UpdateAddressRequest
from ...domain.dto.responses.address_responses import AddressUpdatedResponse
from ...domain.exceptions.user_exceptions import UserException, UserNotFoundException


class UpdateAddressUseCase:
    """Caso de uso para actualizar una dirección"""
    
    def __init__(self, address_repository: AddressRepository):
        self.address_repository = address_repository
    
    async def execute(self, address_id: UUID, request: UpdateAddressRequest) -> AddressUpdatedResponse:
        """Ejecutar el caso de uso"""
        try:
            # Verificar que la dirección existe
            existing_address = await self.address_repository.get_by_id(address_id)
            if not existing_address:
                raise UserNotFoundException(f"Dirección con ID {address_id} no encontrada")
            
            # Crear entidad Address con datos actualizados
            updated_address = Address(
                id=existing_address.id,
                street=request.street or existing_address.street,
                city_id=request.city_id or existing_address.city_id,
                state_id=request.state_id or existing_address.state_id,
                country_id=request.country_id or existing_address.country_id,
                postal_code=request.postal_code if request.postal_code is not None else existing_address.postal_code,
                additional_info=request.additional_info if request.additional_info is not None else existing_address.additional_info
            )
            
            # Actualizar en el repositorio
            result = await self.address_repository.update(address_id, updated_address)
            
            if not result:
                raise UserException("Error al actualizar la dirección")
            
            return AddressUpdatedResponse(
                id=address_id,
                message="Dirección actualizada exitosamente"
            )
            
        except UserNotFoundException:
            raise
        except Exception as e:
            raise UserException(f"Error inesperado al actualizar dirección: {str(e)}") 