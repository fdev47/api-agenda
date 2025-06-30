"""
Caso de uso para eliminar un tipo de sector
"""
from ...domain.interfaces.sector_type_repository import SectorTypeRepository
from ...domain.exceptions import SectorTypeNotFoundException


class DeleteSectorTypeUseCase:
    """Caso de uso para eliminar un tipo de sector"""
    
    def __init__(self, sector_type_repository: SectorTypeRepository):
        self.sector_type_repository = sector_type_repository
    
    async def execute(self, sector_type_id: int) -> bool:
        """Ejecutar el caso de uso"""
        
        # Verificar que el tipo de sector existe
        existing_sector_type = await self.sector_type_repository.get_by_id(sector_type_id)
        
        if not existing_sector_type:
            raise SectorTypeNotFoundException(
                f"No se encontró el tipo de sector con ID {sector_type_id}",
                entity_id=sector_type_id
            )
        
        # Eliminar el tipo de sector
        await self.sector_type_repository.delete(sector_type_id)
        
        return True 