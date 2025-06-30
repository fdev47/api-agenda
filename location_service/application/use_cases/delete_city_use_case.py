"""
Caso de uso para eliminar una ciudad
"""
from typing import Optional
from ...domain.interfaces.city_repository import CityRepository
from ...domain.exceptions import CityNotFoundException


class DeleteCityUseCase:
    """Caso de uso para eliminar una ciudad"""
    
    def __init__(self, city_repository: CityRepository):
        self.city_repository = city_repository
    
    async def execute(self, city_id: int) -> bool:
        """Ejecutar el caso de uso"""
        
        # Buscar la ciudad existente
        existing_city = await self.city_repository.get_by_id(city_id)
        if not existing_city:
            raise CityNotFoundException(city_id=str(city_id))
        
        # Eliminar la ciudad (soft delete)
        await self.city_repository.delete(city_id)
        return True 