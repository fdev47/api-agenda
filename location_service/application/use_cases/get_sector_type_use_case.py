"""
Caso de uso para obtener un tipo de sector por ID
"""
from ...domain.interfaces.sector_type_repository import SectorTypeRepository
from ...domain.dto.responses.sector_type_responses import SectorTypeResponse
from ...domain.exceptions import SectorTypeNotFoundException


class GetSectorTypeUseCase:
    """Caso de uso para obtener un tipo de sector por ID"""
    
    def __init__(self, sector_type_repository: SectorTypeRepository):
        self.sector_type_repository = sector_type_repository
    
    async def execute(self, sector_type_id: int) -> SectorTypeResponse:
        """Ejecutar el caso de uso"""
        
        # Buscar el tipo de sector en el repositorio
        sector_type = await self.sector_type_repository.get_by_id(sector_type_id)
        
        if not sector_type:
            raise SectorTypeNotFoundException(
                f"No se encontró el tipo de sector con ID {sector_type_id}",
                entity_id=sector_type_id
            )
        
        # Retornar respuesta
        return SectorTypeResponse(
            id=sector_type.id,
            name=sector_type.name,
            code=sector_type.code,
            created_at=sector_type.created_at,
            updated_at=sector_type.updated_at
        ) 