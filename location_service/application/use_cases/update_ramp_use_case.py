"""
Caso de uso para actualizar una rampa
"""
from datetime import datetime
from ...domain.entities.ramp import Ramp
from ...domain.interfaces.ramp_repository import RampRepository
from ...domain.dto.requests.ramp_requests import UpdateRampRequest
from ...domain.dto.responses.ramp_responses import RampResponse
from ...domain.exceptions import RampNotFoundException, RampAlreadyExistsException


class UpdateRampUseCase:
    """Caso de uso para actualizar una rampa"""
    
    def __init__(self, ramp_repository: RampRepository):
        self.ramp_repository = ramp_repository
    
    async def execute(self, ramp_id: int, request: UpdateRampRequest) -> RampResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener la rampa existente
        existing_ramp = await self.ramp_repository.get_by_id(ramp_id)
        
        if not existing_ramp:
            raise RampNotFoundException(
                f"No se encontró la rampa con ID {ramp_id}",
                entity_id=ramp_id
            )
        
        # Verificar que no existe otra rampa con el mismo nombre en la misma sucursal
        if request.name and request.name != existing_ramp.name:
            exists = await self.ramp_repository.exists_by_name_and_branch(
                name=request.name,
                branch_id=request.branch_id or existing_ramp.branch_id,
                exclude_id=ramp_id
            )
            
            if exists:
                raise RampAlreadyExistsException(
                    f"Ya existe una rampa con el nombre '{request.name}' en la sucursal {request.branch_id or existing_ramp.branch_id}",
                    name=request.name,
                    branch_id=request.branch_id or existing_ramp.branch_id
                )
        
        # Crear entidad actualizada
        updated_ramp = Ramp(
            id=ramp_id,
            name=request.name or existing_ramp.name,
            is_available=request.is_available if request.is_available is not None else existing_ramp.is_available,
            branch_id=request.branch_id or existing_ramp.branch_id,
            created_at=existing_ramp.created_at,
            updated_at=datetime.utcnow()
        )
        
        # Actualizar en el repositorio
        saved_ramp = await self.ramp_repository.update(updated_ramp)
        
        # Retornar respuesta
        return RampResponse(
            id=saved_ramp.id,
            name=saved_ramp.name,
            is_available=saved_ramp.is_available,
            branch_id=saved_ramp.branch_id,
            created_at=saved_ramp.created_at,
            updated_at=saved_ramp.updated_at
        ) 