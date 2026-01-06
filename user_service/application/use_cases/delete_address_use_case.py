"""
Caso de uso para eliminar una dirección
"""
from uuid import UUID
from ...domain.interfaces.address_repository import AddressRepository
from ...domain.dto.responses.address_responses import AddressDeletedResponse
from ...domain.exceptions.user_exceptions import UserException, UserNotFoundException


class DeleteAddressUseCase:
    """Caso de uso para eliminar una dirección"""
    
    def __init__(self, address_repository: AddressRepository):
        self.address_repository = address_repository
    
    async def execute(self, address_id: UUID) -> AddressDeletedResponse:
        """Ejecutar el caso de uso"""
        try:
            existing_address = await self.address_repository.get_by_id(address_id)
            if not existing_address:
                raise UserNotFoundException(f"Dirección con ID {address_id} no encontrada")
            
            success = await self.address_repository.delete(address_id)
            
            if not success:
                raise UserException("Error al eliminar la dirección")
            
            return AddressDeletedResponse(
                id=address_id,
                message="Dirección eliminada exitosamente"
            )
            
        except UserNotFoundException:
            raise
        except Exception as e:
            raise UserException(f"Error inesperado al eliminar dirección: {str(e)}") 