"""
Caso de uso para eliminar una rampa
"""
from ...domain.entities.ramp import Ramp
from ...domain.interfaces.ramp_repository import RampRepository
from ...domain.dto.responses.ramp_response import RampResponse
from ...domain.exceptions import RampNotFoundException


class DeleteRampUseCase:
    """Caso de uso para eliminar una rampa"""
    
    def __init__(self, ramp_repository: RampRepository):
        self.ramp_repository = ramp_repository
    
    async def execute(self, ramp_id: int) -> RampResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener la rampa existente
        existing_ramp = await self.ramp_repository.get_by_id(ramp_id)
        
        if not existing_ramp:
            raise RampNotFoundException(
                f"Rampa con ID {ramp_id} no encontrada",
                entity_id=ramp_id
            )
        
        # Eliminar del repositorio
        deleted = await self.ramp_repository.delete(ramp_id)
        
        if not deleted:
            raise RampNotFoundException(
                f"No se pudo eliminar la rampa con ID {ramp_id}",
                entity_id=ramp_id
            )
        
        # Retornar respuesta con los datos de la rampa eliminada
        return RampResponse(
            id=existing_ramp.id,
            name=existing_ramp.name,
            is_available=existing_ramp.is_available,
            branch_id=existing_ramp.branch_id,
            created_at=existing_ramp.created_at,
            updated_at=existing_ramp.updated_at
        ) 