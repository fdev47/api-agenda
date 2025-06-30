"""
Caso de uso para obtener un sector por ID
"""
from ...domain.interfaces.sector_repository import SectorRepository
from ...domain.dto.responses.sector_responses import SectorResponse
from ...domain.exceptions import SectorNotFoundException


class GetSectorUseCase:
    """Caso de uso para obtener un sector por ID"""
    
    def __init__(self, sector_repository: SectorRepository):
        self.sector_repository = sector_repository
    
    async def execute(self, sector_id: int) -> SectorResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener el sector del repositorio
        sector = await self.sector_repository.get_by_id(sector_id)
        
        if not sector:
            raise SectorNotFoundException(
                f"No se encontró el sector con ID {sector_id}",
                entity_id=sector_id
            )
        
        # Retornar respuesta
        return SectorResponse(
            id=sector.id,
            name=sector.name,
            description=sector.description,
            branch_id=sector.branch_id,
            sector_type_id=sector.sector_type_id,
            measurement_unit=sector.measurement_unit.value,
            created_at=sector.created_at,
            updated_at=sector.updated_at
        ) 