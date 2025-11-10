"""
Caso de uso para actualizar un horario de rampa
"""
from ...domain.interfaces.ramp_schedule_repository import RampScheduleRepository
from ...domain.dto.requests.ramp_schedule_requests import UpdateRampScheduleRequest
from ...domain.dto.responses.ramp_schedule_responses import RampScheduleUpdatedResponse
from ...domain.exceptions.ramp_schedule_exceptions import RampScheduleNotFoundException


class UpdateRampScheduleUseCase:
    """Caso de uso para actualizar un horario de rampa"""
    
    def __init__(self, ramp_schedule_repository: RampScheduleRepository):
        self.ramp_schedule_repository = ramp_schedule_repository
    
    async def execute(self, schedule_id: int, request: UpdateRampScheduleRequest) -> RampScheduleUpdatedResponse:
        """Ejecutar el caso de uso"""
        
        # Buscar el horario existente
        existing_schedule = await self.ramp_schedule_repository.get_by_id(schedule_id)
        
        if not existing_schedule:
            raise RampScheduleNotFoundException(schedule_id)
        
        # Actualizar campos
        if request.day_of_week is not None:
            existing_schedule.day_of_week = request.day_of_week
        
        if request.name is not None:
            existing_schedule.update_name(request.name)
        
        if request.start_time is not None or request.end_time is not None:
            start_time = request.start_time if request.start_time is not None else existing_schedule.start_time
            end_time = request.end_time if request.end_time is not None else existing_schedule.end_time
            existing_schedule.update_times(start_time, end_time)
        
        if request.is_active is not None:
            if request.is_active:
                existing_schedule.activate()
            else:
                existing_schedule.deactivate()
        
        # Guardar cambios
        updated_schedule = await self.ramp_schedule_repository.update(existing_schedule)
        
        # Retornar respuesta
        return RampScheduleUpdatedResponse(
            id=updated_schedule.id,
            ramp_id=updated_schedule.ramp_id,
            day_of_week=updated_schedule.day_of_week,
            day_name=updated_schedule.get_day_name(),
            name=updated_schedule.name,
            start_time=updated_schedule.start_time,
            end_time=updated_schedule.end_time,
            is_active=updated_schedule.is_active,
            message="Horario actualizado exitosamente"
        )

