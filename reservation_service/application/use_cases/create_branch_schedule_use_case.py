from typing import Optional
from datetime import datetime

from ...domain.interfaces import ScheduleRepository
from ...domain.entities.schedule import BranchSchedule, DayOfWeek
from ...domain.dto.requests.schedule_requests import CreateBranchScheduleRequest
from ...domain.dto.responses.schedule_responses import CreateBranchScheduleResponse, BranchScheduleResponse
from ...domain.exceptions.schedule_exceptions import (
    ScheduleAlreadyExistsException,
    ScheduleOverlapException
)


class CreateBranchScheduleUseCase:
    """Caso de uso para crear un horario de sucursal"""
    
    def __init__(self, schedule_repository: ScheduleRepository):
        self.schedule_repository = schedule_repository
    
    async def execute(self, request: CreateBranchScheduleRequest) -> CreateBranchScheduleResponse:
        """Ejecutar el caso de uso"""
        
        # Verificar si ya existe un horario para esta sucursal y día
        existing_schedule = await self.schedule_repository.get_by_branch_and_day(
            request.branch_id, 
            request.day_of_week
        )
        
        if existing_schedule:
            raise ScheduleAlreadyExistsException(
                request.branch_id, 
                request.day_of_week.get_name()
            )
        
        # Verificar solapamientos con otros horarios del mismo día
        existing_schedules = await self.schedule_repository.list_by_branch(
            request.branch_id, 
            day_of_week=request.day_of_week
        )
        
        new_schedule = BranchSchedule(
            branch_id=request.branch_id,
            day_of_week=request.day_of_week,
            start_time=request.start_time,
            end_time=request.end_time,
            interval_minutes=request.interval_minutes,
            is_active=request.is_active
        )
        
        # Verificar solapamientos
        for existing in existing_schedules:
            if new_schedule.overlaps_with(existing):
                raise ScheduleOverlapException(
                    request.branch_id,
                    request.day_of_week.get_name(),
                    str(request.start_time),
                    str(request.end_time)
                )
        
        # Crear el horario
        created_schedule = await self.schedule_repository.create(new_schedule)
        
        return CreateBranchScheduleResponse(
            id=created_schedule.id,
            message="Horario creado exitosamente"
        )
    
    def to_response(self, schedule: BranchSchedule) -> BranchScheduleResponse:
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