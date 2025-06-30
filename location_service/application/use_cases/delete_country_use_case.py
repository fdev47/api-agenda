"""
Caso de uso para eliminar un país
"""
from typing import Optional
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.interfaces.state_repository import StateRepository
from ...domain.exceptions import CountryNotFoundException


class DeleteCountryUseCase:
    """Caso de uso para eliminar un país"""
    
    def __init__(self, country_repository: CountryRepository, state_repository: StateRepository):
        self.country_repository = country_repository
        self.state_repository = state_repository
    
    async def execute(self, country_id: int) -> bool:
        """Ejecutar el caso de uso"""
        
        # Buscar el país existente
        existing_country = await self.country_repository.get_by_id(country_id)
        if not existing_country:
            raise CountryNotFoundException(country_id=str(country_id))
        
        # Verificar si tiene estados asociados
        states = await self.state_repository.get_by_country_id(country_id)
        if states:
            # Si tiene estados, solo hacer soft delete
            await self.country_repository.delete(country_id)
            return True
        else:
            # Si no tiene estados, eliminar completamente
            await self.country_repository.delete(country_id)
            return True 