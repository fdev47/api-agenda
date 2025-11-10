"""
Caso de uso para crear un horario de rampa
"""
from datetime import datetime
from ...domain.entities.ramp_schedule import RampSchedule
from ...domain.interfaces.ramp_schedule_repository import RampScheduleRepository
from ...domain.dto.requests.ramp_schedule_requests import CreateRampScheduleRequest
from ...domain.dto.responses.ramp_schedule_responses import RampScheduleCreatedResponse


class CreateRampScheduleUseCase:
    """Caso de uso para crear un horario de rampa"""
    
    def __init__(self, ramp_schedule_repository: RampScheduleRepository):
        self.ramp_schedule_repository = ramp_schedule_repository
    
    async def execute(self, request: CreateRampScheduleRequest) -> RampScheduleCreatedResponse:
        """Ejecutar el caso de uso"""
        
        # Crear entidad del dominio
        schedule = RampSchedule(
            id=0,  # Se asignará automáticamente
            ramp_id=request.ramp_id,
            day_of_week=request.day_of_week,
            name=request.name,
            start_time=request.start_time,
            end_time=request.end_time,
            is_active=request.is_active,
            created_at=datetime.utcnow()
        )
        
        # Guardar en el repositorio
        created_schedule = await self.ramp_schedule_repository.create(schedule)
        
        # Retornar respuesta
        return RampScheduleCreatedResponse(
            id=created_schedule.id,
            ramp_id=created_schedule.ramp_id,
            day_of_week=created_schedule.day_of_week,
            day_name=created_schedule.get_day_name(),
            name=created_schedule.name,
            start_time=created_schedule.start_time,
            end_time=created_schedule.end_time,
            is_active=created_schedule.is_active,
            message="Horario creado exitosamente"
        )

