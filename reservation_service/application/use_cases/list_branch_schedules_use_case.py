"""
Use case para listar horarios de sucursal
"""
from typing import List
from ...domain.entities.day_of_week import DayOfWeek
from ...domain.dto.requests.schedule_requests import GetBranchSchedulesRequest
from ...domain.dto.responses.schedule_responses import BranchScheduleListResponse, BranchScheduleResponse
from ...domain.interfaces.schedule_repository import ScheduleRepository


class ListBranchSchedulesUseCase:
    """Caso de uso para listar horarios de una sucursal"""
    
    def __init__(self, schedule_repository: ScheduleRepository):
        self.schedule_repository = schedule_repository
    
    async def execute(self, request: GetBranchSchedulesRequest) -> BranchScheduleListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener horarios con filtros
        schedules = await self.schedule_repository.list_by_branch(
            branch_id=request.branch_id,
            day_of_week=request.day_of_week,
            is_active=request.is_active
        )
        
        # Convertir a DTOs de respuesta
        schedule_responses = [self.to_response(schedule) for schedule in schedules]
        
        return BranchScheduleListResponse(
            schedules=schedule_responses,
            total=len(schedule_responses),
            branch_id=request.branch_id
        )
    
    def to_response(self, schedule) -> BranchScheduleResponse:
        """Convertir entidad a DTO de respuesta"""
        try:
            response = BranchScheduleResponse(
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
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise 