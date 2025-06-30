from typing import Dict, Any
from datetime import datetime

from ...domain.interfaces import ScheduleRepository
from ...domain.entities.schedule import DayOfWeek
from ...domain.dto.responses.schedule_responses import DeleteBranchScheduleResponse
from ...domain.exceptions.schedule_exceptions import ScheduleNotFoundException
from .validate_schedule_changes_use_case import ValidateScheduleChangesUseCase


class DeleteBranchScheduleWithValidationUseCase:
    """Caso de uso para eliminar un horario de sucursal con validación de reservas"""
    
    def __init__(self, schedule_repository: ScheduleRepository, validate_changes_use_case: ValidateScheduleChangesUseCase):
        self.schedule_repository = schedule_repository
        self.validate_changes_use_case = validate_changes_use_case
    
    async def execute(self, schedule_id: int, auto_reschedule: bool = False) -> Dict[str, Any]:
        """Ejecutar el caso de uso"""
        
        # Obtener el horario actual
        current_schedule = await self.schedule_repository.get_by_id(schedule_id)
        if not current_schedule:
            raise ScheduleNotFoundException(schedule_id=schedule_id)
        
        # Validar el impacto de eliminar el horario (equivalente a desactivar)
        impact_analysis = await self.validate_changes_use_case.execute(
            branch_id=current_schedule.branch_id,
            day_of_week=current_schedule.day_of_week,
            new_start_time=None,
            new_end_time=None,
            is_active=False  # Desactivar el horario
        )
        
        # Si hay reservas afectadas y no se permite auto-reschedule, retornar análisis
        if impact_analysis["requires_rescheduling"] and not auto_reschedule:
            return {
                "success": False,
                "message": "No se puede eliminar el horario porque afectaría reservas existentes",
                "impact_analysis": impact_analysis,
                "requires_confirmation": True
            }
        
        # Aplicar cambios y actualizar reservas afectadas si es necesario
        if impact_analysis["requires_rescheduling"] and auto_reschedule:
            schedule_changes_result = await self.validate_changes_use_case.apply_schedule_changes(
                branch_id=current_schedule.branch_id,
                day_of_week=current_schedule.day_of_week,
                new_start_time=None,
                new_end_time=None,
                is_active=False,
                auto_reschedule=True
            )
        
        # Eliminar el horario
        deleted = await self.schedule_repository.delete(schedule_id)
        
        if not deleted:
            raise ScheduleNotFoundException(schedule_id=schedule_id)
        
        return {
            "success": True,
            "message": "Horario eliminado exitosamente",
            "schedule_id": schedule_id,
            "impact_analysis": impact_analysis,
            "reservations_updated": impact_analysis["impacted_reservations"] if auto_reschedule else 0
        }
    
    async def validate_deletion(self, schedule_id: int) -> Dict[str, Any]:
        """Solo validar el impacto sin eliminar"""
        
        # Obtener el horario actual
        current_schedule = await self.schedule_repository.get_by_id(schedule_id)
        if not current_schedule:
            raise ScheduleNotFoundException(schedule_id=schedule_id)
        
        # Validar el impacto de eliminar el horario
        impact_analysis = await self.validate_changes_use_case.execute(
            branch_id=current_schedule.branch_id,
            day_of_week=current_schedule.day_of_week,
            new_start_time=None,
            new_end_time=None,
            is_active=False
        )
        
        return {
            "schedule_id": schedule_id,
            "branch_id": current_schedule.branch_id,
            "day_of_week": current_schedule.day_of_week.value,
            "day_name": current_schedule.day_of_week.get_name(),
            "current_schedule": {
                "start_time": current_schedule.start_time.strftime("%H:%M"),
                "end_time": current_schedule.end_time.strftime("%H:%M"),
                "interval_minutes": current_schedule.interval_minutes,
                "is_active": current_schedule.is_active
            },
            "impact_analysis": impact_analysis,
            "can_delete": len(impact_analysis["impacted_reservation_ids"]) == 0,
            "requires_rescheduling": impact_analysis["requires_rescheduling"]
        } 