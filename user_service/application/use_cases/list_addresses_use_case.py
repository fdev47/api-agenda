"""
Caso de uso para listar direcciones
"""
from ...domain.interfaces.address_repository import AddressRepository
from ...domain.dto.responses.address_responses import AddressListResponse, AddressResponse
from ...domain.exceptions.user_exceptions import UserException


class ListAddressesUseCase:
    """Caso de uso para listar direcciones"""
    
    def __init__(self, address_repository: AddressRepository):
        self.address_repository = address_repository
    
    async def execute(self) -> AddressListResponse:
        """Ejecutar el caso de uso"""
        try:
            # Obtener todas las direcciones del repositorio
            addresses = await self.address_repository.get_all()
            
            # Convertir a DTOs de respuesta
            address_responses = [
                AddressResponse.model_validate(address) for address in addresses
            ]
            
            return AddressListResponse(
                addresses=address_responses,
                total=len(address_responses)
            )
            
        except Exception as e:
            raise UserException(f"Error inesperado al listar direcciones: {str(e)}") 