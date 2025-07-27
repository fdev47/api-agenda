"""
Caso de uso para obtener una dirección por ID
"""
from uuid import UUID
from ...domain.interfaces.address_repository import AddressRepository
from ...domain.dto.responses.address_responses import AddressResponse
from ...domain.exceptions.user_exceptions import UserException, UserNotFoundException


class GetAddressUseCase:
    """Caso de uso para obtener una dirección por ID"""
    
    def __init__(self, address_repository: AddressRepository):
        self.address_repository = address_repository
    
    async def execute(self, address_id: UUID) -> AddressResponse:
        """Ejecutar el caso de uso"""
        try:
            # Obtener dirección del repositorio
            address = await self.address_repository.get_by_id(address_id)
            
            if not address:
                raise UserNotFoundException(f"Dirección con ID {address_id} no encontrada")
            
            return AddressResponse.model_validate(address)
            
        except UserNotFoundException:
            raise
        except Exception as e:
            raise UserException(f"Error inesperado al obtener dirección: {str(e)}") 