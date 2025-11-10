"""
Caso de uso para obtener todos los horarios de una rampa
"""
from typing import List
from ...domain.interfaces.ramp_schedule_repository import RampScheduleRepository
from ...domain.dto.responses.ramp_schedule_responses import RampScheduleResponse


class GetRampSchedulesByRampUseCase:
    """Caso de uso para obtener todos los horarios de una rampa"""
    
    def __init__(self, ramp_schedule_repository: RampScheduleRepository):
        self.ramp_schedule_repository = ramp_schedule_repository
    
    async def execute(self, ramp_id: int) -> List[RampScheduleResponse]:
        """Ejecutar el caso de uso"""
        
        # Obtener horarios del repositorio
        schedules = await self.ramp_schedule_repository.get_by_ramp_id(ramp_id)
        
        # Convertir a responses
        return [
            RampScheduleResponse(
                id=schedule.id,
                ramp_id=schedule.ramp_id,
                day_of_week=schedule.day_of_week,
                day_name=schedule.get_day_name(),
                name=schedule.name,
                start_time=schedule.start_time,
                end_time=schedule.end_time,
                is_active=schedule.is_active,
                created_at=schedule.created_at,
                updated_at=schedule.updated_at
            )
            for schedule in schedules
        ]

