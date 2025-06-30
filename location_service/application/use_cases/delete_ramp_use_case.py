"""
Caso de uso para eliminar una rampa
"""
from ...domain.interfaces.ramp_repository import RampRepository
from ...domain.exceptions import RampNotFoundException


class DeleteRampUseCase:
    """Caso de uso para eliminar una rampa"""
    
    def __init__(self, ramp_repository: RampRepository):
        self.ramp_repository = ramp_repository
    
    async def execute(self, ramp_id: int) -> bool:
        """Ejecutar el caso de uso"""
        
        # Verificar que la rampa existe
        existing_ramp = await self.ramp_repository.get_by_id(ramp_id)
        
        if not existing_ramp:
            raise RampNotFoundException(
                f"No se encontró la rampa con ID {ramp_id}",
                entity_id=ramp_id
            )
        
        # Eliminar del repositorio
        deleted = await self.ramp_repository.delete(ramp_id)
        
        return deleted 