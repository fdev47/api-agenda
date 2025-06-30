"""
Caso de uso para eliminar un sector
"""
from ...domain.interfaces.sector_repository import SectorRepository
from ...domain.exceptions import SectorNotFoundException


class DeleteSectorUseCase:
    """Caso de uso para eliminar un sector"""
    
    def __init__(self, sector_repository: SectorRepository):
        self.sector_repository = sector_repository
    
    async def execute(self, sector_id: int) -> bool:
        """Ejecutar el caso de uso"""
        
        # Verificar que el sector existe
        existing_sector = await self.sector_repository.get_by_id(sector_id)
        
        if not existing_sector:
            raise SectorNotFoundException(
                f"No se encontró el sector con ID {sector_id}",
                entity_id=sector_id
            )
        
        # Eliminar del repositorio
        deleted = await self.sector_repository.delete(sector_id)
        
        return deleted 