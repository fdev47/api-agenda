"""
Caso de uso para obtener una rampa por ID
"""
from ...domain.entities.ramp import Ramp
from ...domain.interfaces.ramp_repository import RampRepository
from ...domain.dto.responses.ramp_response import RampResponse
from ...domain.exceptions import RampNotFoundException


class GetRampUseCase:
    """Caso de uso para obtener una rampa por ID"""
    
    def __init__(self, ramp_repository: RampRepository):
        self.ramp_repository = ramp_repository
    
    async def execute(self, ramp_id: int) -> RampResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener la rampa del repositorio
        ramp = await self.ramp_repository.get_by_id(ramp_id)
        
        if not ramp:
            raise RampNotFoundException(
                f"Rampa con ID {ramp_id} no encontrada",
                entity_id=ramp_id
            )
        
        # Retornar respuesta
        return RampResponse(
            id=ramp.id,
            name=ramp.name,
            is_available=ramp.is_available,
            branch_id=ramp.branch_id,
            created_at=ramp.created_at,
            updated_at=ramp.updated_at
        ) 