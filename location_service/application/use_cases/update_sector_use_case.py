"""
Caso de uso para actualizar un sector
"""
from datetime import datetime
from ...domain.entities.sector import Sector
from ...domain.interfaces.sector_repository import SectorRepository
from ...domain.interfaces.sector_type_repository import SectorTypeRepository
from ...domain.dto.requests.sector_requests import UpdateSectorRequest
from ...domain.dto.responses.sector_responses import SectorResponse
from ...domain.exceptions import SectorNotFoundException, SectorAlreadyExistsException, SectorTypeNotFoundException


class UpdateSectorUseCase:
    """Caso de uso para actualizar un sector"""
    
    def __init__(self, sector_repository: SectorRepository, sector_type_repository: SectorTypeRepository):
        self.sector_repository = sector_repository
        self.sector_type_repository = sector_type_repository
    
    async def execute(self, sector_id: int, request: UpdateSectorRequest) -> SectorResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener el sector existente
        existing_sector = await self.sector_repository.get_by_id(sector_id)
        
        if not existing_sector:
            raise SectorNotFoundException(
                f"No se encontró el sector con ID {sector_id}",
                entity_id=sector_id
            )
        
        # Verificar que el tipo de sector existe si se está actualizando
        if request.sector_type_id:
            sector_type = await self.sector_type_repository.get_by_id(request.sector_type_id)
            if not sector_type:
                raise SectorTypeNotFoundException(
                    f"No se encontró el tipo de sector con ID {request.sector_type_id}",
                    entity_id=request.sector_type_id
                )
        
        # Verificar que no existe otro sector con el mismo nombre en la misma sucursal
        if request.name and request.name != existing_sector.name:
            exists = await self.sector_repository.exists_by_name_and_branch(
                name=request.name,
                branch_id=request.branch_id or existing_sector.branch_id,
                exclude_id=sector_id
            )
            
            if exists:
                raise SectorAlreadyExistsException(
                    f"Ya existe un sector con el nombre '{request.name}' en la sucursal {request.branch_id or existing_sector.branch_id}",
                    name=request.name,
                    branch_id=request.branch_id or existing_sector.branch_id
                )
        
        # Crear entidad actualizada
        updated_sector = Sector(
            id=sector_id,
            name=request.name or existing_sector.name,
            description=request.description or existing_sector.description,
            branch_id=request.branch_id or existing_sector.branch_id,
            sector_type_id=request.sector_type_id or existing_sector.sector_type_id,
            measurement_unit=request.measurement_unit or existing_sector.measurement_unit,
            created_at=existing_sector.created_at,
            updated_at=datetime.utcnow()
        )
        
        # Actualizar en el repositorio
        saved_sector = await self.sector_repository.update(updated_sector)
        
        # Retornar respuesta
        return SectorResponse(
            id=saved_sector.id,
            name=saved_sector.name,
            description=saved_sector.description,
            branch_id=saved_sector.branch_id,
            sector_type_id=saved_sector.sector_type_id,
            measurement_unit=saved_sector.measurement_unit.value,
            created_at=saved_sector.created_at,
            updated_at=saved_sector.updated_at
        ) 