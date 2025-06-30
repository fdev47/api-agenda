from typing import Optional

from ...domain.interfaces import ScheduleRepository
from ...domain.dto.responses.schedule_responses import BranchScheduleResponse
from ...domain.exceptions.schedule_exceptions import ScheduleNotFoundException


class GetBranchScheduleUseCase:
    """Caso de uso para obtener un horario de sucursal por ID"""
    
    def __init__(self, schedule_repository: ScheduleRepository):
        self.schedule_repository = schedule_repository
    
    async def execute(self, schedule_id: int) -> BranchScheduleResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener el horario
        schedule = await self.schedule_repository.get_by_id(schedule_id)
        
        if not schedule:
            raise ScheduleNotFoundException(schedule_id=schedule_id)
        
        return self.to_response(schedule)
    
    def to_response(self, schedule) -> BranchScheduleResponse:
        """Convertir entidad a DTO de respuesta"""
        return BranchScheduleResponse(
            id=schedule.id,
            branch_id=schedule.branch_id,
            day_of_week=schedule.day_of_week,
            day_name=schedule.get_day_name(),
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            interval_minutes=schedule.interval_minutes,
            is_active=schedule.is_active,
            duration_minutes=schedule.duration_minutes(),
            duration_hours=schedule.duration_hours(),
            created_at=schedule.created_at,
            updated_at=schedule.updated_at
        ) 