"""
Caso de uso para listar horarios de rampas
"""
from ...domain.interfaces.ramp_schedule_repository import RampScheduleRepository
from ...domain.dto.requests.ramp_schedule_requests import RampScheduleFilterRequest
from ...domain.dto.responses.ramp_schedule_responses import RampScheduleResponse, RampScheduleListResponse


class ListRampSchedulesUseCase:
    """Caso de uso para listar horarios de rampas"""
    
    def __init__(self, ramp_schedule_repository: RampScheduleRepository):
        self.ramp_schedule_repository = ramp_schedule_repository
    
    async def execute(self, filter_request: RampScheduleFilterRequest) -> RampScheduleListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener horarios del repositorio
        schedules, total = await self.ramp_schedule_repository.list(filter_request)
        
        # Convertir a responses
        schedule_responses = [
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
        
        # Calcular paginación
        page = (filter_request.offset // filter_request.limit) + 1
        
        return RampScheduleListResponse(
            schedules=schedule_responses,
            total=total,
            page=page,
            size=len(schedule_responses)
        )

