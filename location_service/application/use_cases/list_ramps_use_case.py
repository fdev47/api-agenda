"""
Caso de uso para listar rampas
"""
from typing import List
from ...domain.interfaces.ramp_repository import RampRepository
from ...domain.dto.requests.ramp_requests import RampFilterRequest
from ...domain.dto.responses.ramp_responses import RampResponse, RampListResponse


class ListRampsUseCase:
    """Caso de uso para listar rampas"""
    
    def __init__(self, ramp_repository: RampRepository):
        self.ramp_repository = ramp_repository
    
    async def execute(self, filter_request: RampFilterRequest) -> RampListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener rampas del repositorio
        ramps, total = await self.ramp_repository.list(filter_request)
        
        # Convertir a respuestas
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
            items=ramp_responses,
            total=total,
            page=filter_request.page,
            size=filter_request.limit,
            pages=(total + filter_request.limit - 1) // filter_request.limit
        ) 