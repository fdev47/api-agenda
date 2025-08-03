"""
Caso de uso para crear una rampa
"""
from datetime import datetime
from ...domain.entities.ramp import Ramp
from ...domain.interfaces.ramp_repository import RampRepository
from ...domain.dto.requests.create_ramp_request import CreateRampRequest
from ...domain.dto.responses.ramp_response import RampResponse
from ...domain.exceptions import RampAlreadyExistsException


class CreateRampUseCase:
    """Caso de uso para crear una rampa"""
    
    def __init__(self, ramp_repository: RampRepository):
        self.ramp_repository = ramp_repository
    
    async def execute(self, request: CreateRampRequest) -> RampResponse:
        """Ejecutar el caso de uso"""
        
        # Verificar que no existe una rampa con el mismo nombre en la misma sucursal
        exists = await self.ramp_repository.exists_by_name_and_branch(
            name=request.name,
            branch_id=request.branch_id
        )
        
        if exists:
            raise RampAlreadyExistsException(
                f"Ya existe una rampa con el nombre '{request.name}' en la sucursal {request.branch_id}",
                name=request.name,
                branch_id=request.branch_id
            )
        
        # Crear entidad del dominio
        ramp = Ramp(
            id=0,  # Se asignará automáticamente
            name=request.name,
            is_available=request.is_available,
            branch_id=request.branch_id,
            created_at=datetime.utcnow()
        )
        
        # Guardar en el repositorio
        created_ramp = await self.ramp_repository.create(ramp)
        
        # Retornar respuesta
        return RampResponse(
            id=created_ramp.id,
            name=created_ramp.name,
            is_available=created_ramp.is_available,
            branch_id=created_ramp.branch_id,
            created_at=created_ramp.created_at,
            updated_at=created_ramp.updated_at
        ) 