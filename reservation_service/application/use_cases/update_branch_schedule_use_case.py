"""
Use case para actualizar horario de sucursal
"""
from typing import Optional
from datetime import datetime
import logging

from ...domain.entities.day_of_week import DayOfWeek
from ...domain.dto.requests.schedule_requests import UpdateBranchScheduleRequest
from ...domain.dto.responses.schedule_responses import UpdateBranchScheduleResponse, BranchScheduleResponse
from ...domain.dto.responses.schedule_validation_responses import UpdateScheduleResult, ValidateScheduleChangesResult
from ...domain.exceptions.schedule_exceptions import (
    ScheduleNotFoundException,
    ScheduleOverlapException,
    InvalidScheduleTimeException,
    InvalidIntervalException
)
from .validate_schedule_changes_use_case import ValidateScheduleChangesUseCase
from ...domain.interfaces.schedule_repository import ScheduleRepository

# Configurar logging
logger = logging.getLogger(__name__)


class UpdateBranchScheduleUseCase:
    """Caso de uso para actualizar un horario de sucursal con validación de reservas"""
    
    def __init__(self, schedule_repository: ScheduleRepository, validate_changes_use_case: ValidateScheduleChangesUseCase):
        self.schedule_repository = schedule_repository
        self.validate_changes_use_case = validate_changes_use_case
    
    async def execute(self, schedule_id: int, request: UpdateBranchScheduleRequest, 
                     auto_reschedule: bool = False) -> UpdateScheduleResult:
        """Ejecutar el caso de uso"""
        logger.info(f"🔄 Iniciando actualización de horario para schedule_id: {schedule_id}")
        logger.info(f"📝 Datos de actualización: {request}")
        logger.info(f"📝 Auto reschedule: {auto_reschedule}")
        
        try:
            logger.info("📝 Obteniendo horario actual...")
            # Obtener el horario actual
            current_schedule = await self.schedule_repository.get_by_id(schedule_id)
            if not current_schedule:
                logger.warning(f"⚠️ Horario no encontrado: {schedule_id}")
                raise ScheduleNotFoundException(schedule_id=schedule_id)
            
            logger.info(f"✅ Horario actual encontrado: branch_id={current_schedule.branch_id}, day_of_week={current_schedule.day_of_week}")
            
            logger.info("🔄 Ejecutando validación de cambios...")
            # Validar el impacto de los cambios antes de aplicarlos
            impact_analysis = await self.validate_changes_use_case.execute(
                branch_id=current_schedule.branch_id,
                day_of_week=current_schedule.day_of_week,
                new_start_time=request.start_time.strftime("%H:%M") if request.start_time else None,
                new_end_time=request.end_time.strftime("%H:%M") if request.end_time else None,
                new_interval_minutes=request.interval_minutes,
                is_active=request.is_active
            )
            logger.info("✅ Validación de cambios completada")
            logger.info(f"📊 Análisis de impacto: requires_rescheduling={impact_analysis.requires_rescheduling}, impacted_reservations={impact_analysis.impact_analysis.impacted_reservations}")
            
            # Si hay reservas afectadas y no se permite auto-reschedule, retornar análisis
            if impact_analysis.requires_rescheduling and not auto_reschedule:
                logger.warning("⚠️ Cambios requieren confirmación debido a reservas afectadas")
                return UpdateScheduleResult(
                    success=False,
                    message="Los cambios afectarían reservas existentes",
                    impact_analysis=impact_analysis,
                    requires_confirmation=True
                )
            
            logger.info("📝 Preparando datos de actualización...")
            # Preparar datos de actualización
            update_data = {}
            if request.day_of_week is not None:
                update_data["day_of_week"] = request.day_of_week
                logger.info(f"📝 Actualizando day_of_week: {request.day_of_week}")
            if request.start_time is not None:
                update_data["start_time"] = request.start_time
                logger.info(f"📝 Actualizando start_time: {request.start_time}")
            if request.end_time is not None:
                update_data["end_time"] = request.end_time
                logger.info(f"📝 Actualizando end_time: {request.end_time}")
            if request.interval_minutes is not None:
                update_data["interval_minutes"] = request.interval_minutes
                logger.info(f"📝 Actualizando interval_minutes: {request.interval_minutes}")
            if request.is_active is not None:
                update_data["is_active"] = request.is_active
                logger.info(f"📝 Actualizando is_active: {request.is_active}")
            
            logger.info(f"📝 Datos de actualización preparados: {update_data}")
            
            # Verificar solapamientos si se cambia el día o horario
            if request.day_of_week or request.start_time or request.end_time:
                logger.info("🔄 Validando solapamientos...")
                await self._validate_no_overlap(current_schedule, update_data)
                logger.info("✅ Validación de solapamientos completada")
            
            # Aplicar cambios de horario y actualizar reservas afectadas si es necesario
            if impact_analysis.requires_rescheduling and auto_reschedule:
                logger.info("🔄 Aplicando cambios de horario con auto-reschedule...")
                schedule_changes_result = await self.validate_changes_use_case.apply_schedule_changes(
                    branch_id=current_schedule.branch_id,
                    day_of_week=current_schedule.day_of_week,
                    new_start_time=request.start_time.strftime("%H:%M") if request.start_time else None,
                    new_end_time=request.end_time.strftime("%H:%M") if request.end_time else None,
                    new_interval_minutes=request.interval_minutes,
                    is_active=request.is_active,
                    auto_reschedule=True
                )
                logger.info("✅ Cambios de horario aplicados con auto-reschedule")
            
            logger.info("🔄 Actualizando horario en base de datos...")
            # Actualizar el horario
            updated_schedule = await self.schedule_repository.update(schedule_id, update_data)
            
            if not updated_schedule:
                logger.warning(f"⚠️ Error al actualizar horario: {schedule_id}")
                raise ScheduleNotFoundException(schedule_id=schedule_id)
            
            logger.info("✅ Horario actualizado exitosamente en base de datos")
            
            # Crear respuesta usando el DTO
            response = UpdateScheduleResult(
                success=True,
                message="Horario actualizado exitosamente",
                schedule=self.to_response(updated_schedule),
                impact_analysis=impact_analysis,
                reservations_updated=impact_analysis.impact_analysis.impacted_reservations if auto_reschedule else 0
            )
            
            logger.info(f"✅ Actualización completada: reservations_updated={response.reservations_updated}")
            return response
            
        except ScheduleNotFoundException as e:
            logger.warning(f"⚠️ Horario no encontrado en execute: {e.message}")
            raise
        except (ScheduleOverlapException, InvalidScheduleTimeException, InvalidIntervalException) as e:
            logger.warning(f"⚠️ Error de validación en execute: {e.message}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado en execute: {str(e)}", exc_info=True)
            raise
    
    async def _validate_no_overlap(self, current_schedule, update_data: dict):
        """Validar que no haya solapamientos con otros horarios"""
        logger.info("🔄 Iniciando validación de solapamientos...")
        
        try:
            # Obtener otros horarios de la misma sucursal
            logger.info(f"📝 Obteniendo otros horarios para branch_id: {current_schedule.branch_id}")
            other_schedules = await self.schedule_repository.list_by_branch(
                current_schedule.branch_id
            )
            logger.info(f"📊 Otros horarios encontrados: {len(other_schedules)}")
            
            # Filtrar el horario actual
            other_schedules = [s for s in other_schedules if s.id != current_schedule.id]
            logger.info(f"📊 Horarios a validar (excluyendo actual): {len(other_schedules)}")
            
            # Crear horario temporal para validación
            logger.info("📝 Creando horario temporal para validación...")
            test_schedule = current_schedule
            for key, value in update_data.items():
                setattr(test_schedule, key, value)
                logger.info(f"📝 Aplicando cambio temporal: {key} = {value}")
            
            # Verificar solapamientos
            logger.info("🔄 Verificando solapamientos...")
            for other_schedule in other_schedules:
                logger.info(f"📝 Comparando con horario {other_schedule.id}: {other_schedule.day_of_week} {other_schedule.start_time}-{other_schedule.end_time}")
                if test_schedule.overlaps_with(other_schedule):
                    logger.warning(f"⚠️ Solapamiento detectado con horario {other_schedule.id}")
                    raise ScheduleOverlapException(
                        current_schedule.branch_id,
                        test_schedule.get_day_name(),
                        str(test_schedule.start_time),
                        str(test_schedule.end_time)
                    )
            
            logger.info("✅ Validación de solapamientos completada sin conflictos")
            
        except ScheduleOverlapException as e:
            logger.warning(f"⚠️ Solapamiento detectado: {e.message}")
            raise
        except Exception as e:
            logger.error(f"❌ Error en validación de solapamientos: {str(e)}", exc_info=True)
            raise
    
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