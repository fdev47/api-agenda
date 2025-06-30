"""
Caso de uso para actualizar un tipo de sector
"""
from ...domain.entities.sector_type import SectorType
from ...domain.interfaces.sector_type_repository import SectorTypeRepository
from ...domain.dto.requests.sector_type_requests import UpdateSectorTypeRequest
from ...domain.dto.responses.sector_type_responses import SectorTypeResponse
from ...domain.exceptions import SectorTypeNotFoundException


class UpdateSectorTypeUseCase:
    """Caso de uso para actualizar un tipo de sector"""
    
    def __init__(self, sector_type_repository: SectorTypeRepository):
        self.sector_type_repository = sector_type_repository
    
    async def execute(self, sector_type_id: int, request: UpdateSectorTypeRequest) -> SectorTypeResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener el tipo de sector existente
        existing_sector_type = await self.sector_type_repository.get_by_id(sector_type_id)
        
        if not existing_sector_type:
            raise SectorTypeNotFoundException(
                f"No se encontró el tipo de sector con ID {sector_type_id}",
                entity_id=sector_type_id
            )
        
        # Actualizar campos si se proporcionan
        if request.name is not None:
            existing_sector_type.update_name(request.name)
        
        if request.code is not None:
            existing_sector_type.update_code(request.code)
        
        # Guardar cambios en el repositorio
        updated_sector_type = await self.sector_type_repository.update(existing_sector_type)
        
        # Retornar respuesta
        return SectorTypeResponse(
            id=updated_sector_type.id,
            name=updated_sector_type.name,
            code=updated_sector_type.code,
            created_at=updated_sector_type.created_at,
            updated_at=updated_sector_type.updated_at
        ) 