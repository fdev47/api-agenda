from typing import Optional, Dict, Any
from datetime import datetime

from ...domain.interfaces import ScheduleRepository
from ...domain.entities.schedule import DayOfWeek
from ...domain.dto.requests.schedule_requests import UpdateBranchScheduleRequest
from ...domain.dto.responses.schedule_responses import UpdateBranchScheduleResponse, BranchScheduleResponse
from ...domain.exceptions.schedule_exceptions import (
    ScheduleNotFoundException,
    ScheduleOverlapException,
    InvalidScheduleTimeException,
    InvalidIntervalException
)
from .validate_schedule_changes_use_case import ValidateScheduleChangesUseCase


class UpdateBranchScheduleUseCase:
    """Caso de uso para actualizar un horario de sucursal con validación de reservas"""
    
    def __init__(self, schedule_repository: ScheduleRepository, validate_changes_use_case: ValidateScheduleChangesUseCase):
        self.schedule_repository = schedule_repository
        self.validate_changes_use_case = validate_changes_use_case
    
    async def execute(self, schedule_id: int, request: UpdateBranchScheduleRequest, 
                     auto_reschedule: bool = False) -> Dict[str, Any]:
        """Ejecutar el caso de uso"""
        
        # Obtener el horario actual
        current_schedule = await self.schedule_repository.get_by_id(schedule_id)
        if not current_schedule:
            raise ScheduleNotFoundException(schedule_id=schedule_id)
        
        # Validar el impacto de los cambios antes de aplicarlos
        impact_analysis = await self.validate_changes_use_case.execute(
            branch_id=current_schedule.branch_id,
            day_of_week=current_schedule.day_of_week,
            new_start_time=request.start_time.strftime("%H:%M") if request.start_time else None,
            new_end_time=request.end_time.strftime("%H:%M") if request.end_time else None,
            new_interval_minutes=request.interval_minutes,
            is_active=request.is_active
        )
        
        # Si hay reservas afectadas y no se permite auto-reschedule, retornar análisis
        if impact_analysis["requires_rescheduling"] and not auto_reschedule:
            return {
                "success": False,
                "message": "Los cambios afectarían reservas existentes",
                "impact_analysis": impact_analysis,
                "requires_confirmation": True
            }
        
        # Preparar datos de actualización
        update_data = {}
        if request.day_of_week is not None:
            update_data["day_of_week"] = request.day_of_week
        if request.start_time is not None:
            update_data["start_time"] = request.start_time
        if request.end_time is not None:
            update_data["end_time"] = request.end_time
        if request.interval_minutes is not None:
            update_data["interval_minutes"] = request.interval_minutes
        if request.is_active is not None:
            update_data["is_active"] = request.is_active
        
        # Verificar solapamientos si se cambia el día o horario
        if request.day_of_week or request.start_time or request.end_time:
            await self._validate_no_overlap(current_schedule, update_data)
        
        # Aplicar cambios de horario y actualizar reservas afectadas si es necesario
        if impact_analysis["requires_rescheduling"] and auto_reschedule:
            schedule_changes_result = await self.validate_changes_use_case.apply_schedule_changes(
                branch_id=current_schedule.branch_id,
                day_of_week=current_schedule.day_of_week,
                new_start_time=request.start_time.strftime("%H:%M") if request.start_time else None,
                new_end_time=request.end_time.strftime("%H:%M") if request.end_time else None,
                new_interval_minutes=request.interval_minutes,
                is_active=request.is_active,
                auto_reschedule=True
            )
        
        # Actualizar el horario
        updated_schedule = await self.schedule_repository.update(schedule_id, update_data)
        
        if not updated_schedule:
            raise ScheduleNotFoundException(schedule_id=schedule_id)
        
        return {
            "success": True,
            "message": "Horario actualizado exitosamente",
            "schedule": self.to_response(updated_schedule),
            "impact_analysis": impact_analysis,
            "reservations_updated": impact_analysis["impacted_reservations"] if auto_reschedule else 0
        }
    
    async def _validate_no_overlap(self, current_schedule, update_data: dict):
        """Validar que no haya solapamientos con otros horarios"""
        # Obtener otros horarios de la misma sucursal
        other_schedules = await self.schedule_repository.list_by_branch(
            current_schedule.branch_id
        )
        
        # Filtrar el horario actual
        other_schedules = [s for s in other_schedules if s.id != current_schedule.id]
        
        # Crear horario temporal para validación
        test_schedule = current_schedule
        for key, value in update_data.items():
            setattr(test_schedule, key, value)
        
        # Verificar solapamientos
        for other_schedule in other_schedules:
            if test_schedule.overlaps_with(other_schedule):
                raise ScheduleOverlapException(
                    current_schedule.branch_id,
                    test_schedule.get_day_name(),
                    str(test_schedule.start_time),
                    str(test_schedule.end_time)
                )
    
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