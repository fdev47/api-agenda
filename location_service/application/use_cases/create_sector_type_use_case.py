"""
Caso de uso para crear un tipo de sector
"""
from datetime import datetime
from ...domain.entities.sector_type import SectorType
from ...domain.interfaces.sector_type_repository import SectorTypeRepository
from ...domain.dto.requests.sector_type_requests import CreateSectorTypeRequest
from ...domain.dto.responses.sector_type_responses import SectorTypeResponse


class CreateSectorTypeUseCase:
    """Caso de uso para crear un tipo de sector"""
    
    def __init__(self, sector_type_repository: SectorTypeRepository):
        self.sector_type_repository = sector_type_repository
    
    async def execute(self, request: CreateSectorTypeRequest) -> SectorTypeResponse:
        """Ejecutar el caso de uso"""
        
        # Crear entidad del dominio
        sector_type = SectorType(
            id=0,  # Se asignará automáticamente
            name=request.name,
            code=request.code,
            measurement_unit=request.measurement_unit,
            merchandise_type=request.merchandise_type,
            created_at=datetime.utcnow()
        )
        
        # Guardar en el repositorio
        created_sector_type = await self.sector_type_repository.create(sector_type)
        
        # Retornar respuesta
        return SectorTypeResponse(
            id=created_sector_type.id,
            name=created_sector_type.name,
            code=created_sector_type.code,
            description=created_sector_type.description,
            measurement_unit=created_sector_type.measurement_unit.value,
            merchandise_type=created_sector_type.merchandise_type,
            is_active=created_sector_type.is_active,
            created_at=created_sector_type.created_at,
            updated_at=created_sector_type.updated_at
        ) 