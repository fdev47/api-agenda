"""
Use case para eliminar horario de sucursal con validación
"""
from typing import Dict, Any, List
from datetime import datetime
import logging

from ...domain.entities.day_of_week import DayOfWeek
from ...domain.dto.responses.schedule_responses import DeleteBranchScheduleResponse
from ...domain.exceptions.schedule_exceptions import ScheduleNotFoundException
from .validate_schedule_changes_use_case import ValidateScheduleChangesUseCase
from ...domain.interfaces.schedule_repository import ScheduleRepository
from ...domain.interfaces.reservation_repository import ReservationRepository

# Configurar logging
logger = logging.getLogger(__name__)


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
        logger.info(f"🔄 Iniciando validación de eliminación para schedule_id: {schedule_id}")
        
        try:
            logger.info("📝 Obteniendo horario actual...")
            # Obtener el horario actual
            current_schedule = await self.schedule_repository.get_by_id(schedule_id)
            if not current_schedule:
                logger.warning(f"⚠️ Horario no encontrado: {schedule_id}")
                raise ScheduleNotFoundException(schedule_id=schedule_id)
            
            logger.info(f"✅ Horario encontrado: branch_id={current_schedule.branch_id}, day_of_week={current_schedule.day_of_week}")
            
            logger.info("🔄 Ejecutando validación de cambios...")
            # Validar el impacto de eliminar el horario
            impact_analysis = await self.validate_changes_use_case.execute(
                branch_id=current_schedule.branch_id,
                day_of_week=current_schedule.day_of_week,
                new_start_time=None,
                new_end_time=None,
                is_active=False
            )
            logger.info("✅ Validación de cambios completada")
            logger.info(f"📊 Análisis de impacto: requires_rescheduling={impact_analysis.get('requires_rescheduling')}, impacted_reservations={len(impact_analysis.get('impacted_reservation_ids', []))}")
            
            # Preparar respuesta
            result = {
                "schedule_id": schedule_id,
                "branch_id": current_schedule.branch_id,
                "day_of_week": current_schedule.day_of_week.value,
                "day_name": DayOfWeek.get_name(current_schedule.day_of_week.value),
                "current_schedule": {
                    "start_time": current_schedule.start_time.strftime("%H:%M"),
                    "end_time": current_schedule.end_time.strftime("%H:%M"),
                    "interval_minutes": current_schedule.interval_minutes,
                    "is_active": current_schedule.is_active
                },
                "impact_analysis": impact_analysis,
                "can_delete": len(impact_analysis["impact_analysis"]["impacted_reservation_ids"]) == 0,
                "requires_rescheduling": impact_analysis["requires_rescheduling"]
            }
            
            logger.info(f"✅ Resultado preparado: can_delete={result['can_delete']}, requires_rescheduling={result['requires_rescheduling']}")
            return result
            
        except ScheduleNotFoundException as e:
            logger.warning(f"⚠️ Horario no encontrado en validate_deletion: {e.message}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado en validate_deletion: {str(e)}", exc_info=True)
            raise 