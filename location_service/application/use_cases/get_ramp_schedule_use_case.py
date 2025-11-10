"""
Caso de uso para obtener un horario de rampa por ID
"""
from ...domain.interfaces.ramp_schedule_repository import RampScheduleRepository
from ...domain.dto.responses.ramp_schedule_responses import RampScheduleResponse
from ...domain.exceptions.ramp_schedule_exceptions import RampScheduleNotFoundException


class GetRampScheduleUseCase:
    """Caso de uso para obtener un horario de rampa por ID"""
    
    def __init__(self, ramp_schedule_repository: RampScheduleRepository):
        self.ramp_schedule_repository = ramp_schedule_repository
    
    async def execute(self, schedule_id: int) -> RampScheduleResponse:
        """Ejecutar el caso de uso"""
        
        # Buscar el horario
        schedule = await self.ramp_schedule_repository.get_by_id(schedule_id)
        
        if not schedule:
            raise RampScheduleNotFoundException(schedule_id)
        
        # Retornar respuesta
        return RampScheduleResponse(
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

