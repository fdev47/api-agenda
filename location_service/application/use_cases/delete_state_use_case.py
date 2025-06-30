"""
Caso de uso para eliminar un estado
"""
from typing import Optional
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.city_repository import CityRepository
from ...domain.exceptions import StateNotFoundException


class DeleteStateUseCase:
    """Caso de uso para eliminar un estado"""
    
    def __init__(self, state_repository: StateRepository, city_repository: CityRepository):
        self.state_repository = state_repository
        self.city_repository = city_repository
    
    async def execute(self, state_id: int) -> bool:
        """Ejecutar el caso de uso"""
        
        # Buscar el estado existente
        existing_state = await self.state_repository.get_by_id(state_id)
        if not existing_state:
            raise StateNotFoundException(state_id=str(state_id))
        
        # Verificar si tiene ciudades asociadas
        cities = await self.city_repository.get_by_state_id(state_id)
        if cities:
            # Si tiene ciudades, solo hacer soft delete
            await self.state_repository.delete(state_id)
            return True
        else:
            # Si no tiene ciudades, eliminar completamente
            await self.state_repository.delete(state_id)
            return True 