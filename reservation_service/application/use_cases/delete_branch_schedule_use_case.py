from ...domain.interfaces import ScheduleRepository
from ...domain.dto.responses.schedule_responses import DeleteBranchScheduleResponse
from ...domain.exceptions.schedule_exceptions import ScheduleNotFoundException


class DeleteBranchScheduleUseCase:
    """Caso de uso para eliminar un horario de sucursal"""
    
    def __init__(self, schedule_repository: ScheduleRepository):
        self.schedule_repository = schedule_repository
    
    async def execute(self, schedule_id: int) -> DeleteBranchScheduleResponse:
        """Ejecutar el caso de uso"""
        
        # Verificar que el horario existe
        existing_schedule = await self.schedule_repository.get_by_id(schedule_id)
        
        if not existing_schedule:
            raise ScheduleNotFoundException(schedule_id=schedule_id)
        
        # Eliminar el horario
        deleted = await self.schedule_repository.delete(schedule_id)
        
        if not deleted:
            raise ScheduleNotFoundException(schedule_id=schedule_id)
        
        return DeleteBranchScheduleResponse(
            id=schedule_id,
            message="Horario eliminado exitosamente"
        ) 