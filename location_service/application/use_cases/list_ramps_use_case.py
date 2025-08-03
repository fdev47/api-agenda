"""
Caso de uso para listar rampas
"""
from typing import List
from ...domain.entities.ramp import Ramp
from ...domain.interfaces.ramp_repository import RampRepository
from ...domain.dto.requests.ramp_filter_request import RampFilterRequest
from ...domain.dto.responses.ramp_list_response import RampListResponse
from ...domain.dto.responses.ramp_response import RampResponse


class ListRampsUseCase:
    """Caso de uso para listar rampas"""
    
    def __init__(self, ramp_repository: RampRepository):
        self.ramp_repository = ramp_repository
    
    async def execute(self, filter_request: RampFilterRequest) -> RampListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener rampas del repositorio
        ramps, total = await self.ramp_repository.list(filter_request)
        
        # Convertir a DTOs de respuesta
        ramp_responses = [
            RampResponse(
                id=ramp.id,
                name=ramp.name,
                is_available=ramp.is_available,
                branch_id=ramp.branch_id,
                created_at=ramp.created_at,
                updated_at=ramp.updated_at
            )
            for ramp in ramps
        ]
        
        # Retornar respuesta
        return RampListResponse(
            ramps=ramp_responses,
            total=total,
            skip=filter_request.skip,
            limit=filter_request.limit
        ) 