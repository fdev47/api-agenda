"""
Caso de uso para eliminar un horario de rampa
"""
from ...domain.interfaces.ramp_schedule_repository import RampScheduleRepository
from ...domain.dto.responses.ramp_schedule_responses import RampScheduleDeletedResponse
from ...domain.exceptions.ramp_schedule_exceptions import RampScheduleNotFoundException


class DeleteRampScheduleUseCase:
    """Caso de uso para eliminar un horario de rampa"""
    
    def __init__(self, ramp_schedule_repository: RampScheduleRepository):
        self.ramp_schedule_repository = ramp_schedule_repository
    
    async def execute(self, schedule_id: int) -> RampScheduleDeletedResponse:
        """Ejecutar el caso de uso"""
        
        # Verificar que el horario existe
        schedule = await self.ramp_schedule_repository.get_by_id(schedule_id)
        
        if not schedule:
            raise RampScheduleNotFoundException(schedule_id)
        
        # Eliminar el horario
        deleted = await self.ramp_schedule_repository.delete(schedule_id)
        
        if not deleted:
            raise RampScheduleNotFoundException(schedule_id)
        
        # Retornar respuesta
        return RampScheduleDeletedResponse(
            id=schedule_id,
            message="Horario eliminado exitosamente"
        )

