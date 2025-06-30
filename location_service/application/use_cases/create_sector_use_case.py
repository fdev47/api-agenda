"""
Caso de uso para crear un sector
"""
from datetime import datetime
from ...domain.entities.sector import Sector
from ...domain.interfaces.sector_repository import SectorRepository
from ...domain.interfaces.sector_type_repository import SectorTypeRepository
from ...domain.dto.requests.sector_requests import CreateSectorRequest
from ...domain.dto.responses.sector_responses import SectorResponse
from ...domain.exceptions import SectorTypeNotFoundException


class CreateSectorUseCase:
    """Caso de uso para crear un sector"""
    
    def __init__(self, sector_repository: SectorRepository, sector_type_repository: SectorTypeRepository):
        self.sector_repository = sector_repository
        self.sector_type_repository = sector_type_repository
    
    async def execute(self, request: CreateSectorRequest) -> SectorResponse:
        """Ejecutar el caso de uso"""
        
        # Verificar que el tipo de sector existe
        sector_type = await self.sector_type_repository.get_by_id(request.sector_type_id)
        if not sector_type:
            raise SectorTypeNotFoundException(
                f"No se encontró el tipo de sector con ID {request.sector_type_id}",
                entity_id=request.sector_type_id
            )
        
        # Crear entidad del dominio
        sector = Sector(
            id=0,  # Se asignará automáticamente
            name=request.name,
            description=request.description,
            branch_id=request.branch_id,
            sector_type_id=request.sector_type_id,
            measurement_unit=request.measurement_unit,
            created_at=datetime.utcnow()
        )
        
        # Guardar en el repositorio
        created_sector = await self.sector_repository.create(sector)
        
        # Retornar respuesta
        return SectorResponse(
            id=created_sector.id,
            name=created_sector.name,
            description=created_sector.description,
            branch_id=created_sector.branch_id,
            sector_type_id=created_sector.sector_type_id,
            measurement_unit=created_sector.measurement_unit.value,
            created_at=created_sector.created_at,
            updated_at=created_sector.updated_at
        ) 