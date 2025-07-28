"""
Use case para validar cambios en horarios
"""
from typing import List, Dict, Any
from datetime import datetime
import logging

from ...domain.entities.day_of_week import DayOfWeek
from ...domain.entities.reservation import Reservation
from ...domain.entities.reservation_status import ReservationStatus
from ...domain.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.dto.responses.schedule_validation_responses import ImpactAnalysisResponse, ValidateScheduleChangesResult
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.interfaces.schedule_repository import ScheduleRepository
from ...domain.exceptions.schedule_exceptions import ScheduleNotFoundException

# Configurar logging
logger = logging.getLogger(__name__)


class ValidateScheduleChangesUseCase:
    """Caso de uso para validar y actualizar reservas afectadas por cambios de horario"""
    
    def __init__(self, schedule_repository: ScheduleRepository, reservation_repository: ReservationRepository):
        self.schedule_repository = schedule_repository
        self.reservation_repository = reservation_repository
    
    async def execute(self, branch_id: int, day_of_week: DayOfWeek, 
                     new_start_time: str = None, new_end_time: str = None,
                     new_interval_minutes: int = None, is_active: bool = None) -> ValidateScheduleChangesResult:
        """Ejecutar validación de cambios de horario"""
        logger.info(f"🔄 Iniciando validación de cambios para branch_id: {branch_id}, day_of_week: {day_of_week}")
        logger.info(f"📝 Parámetros: new_start_time={new_start_time}, new_end_time={new_end_time}, is_active={is_active}")
        
        try:
            logger.info("📝 Obteniendo horario actual...")
            # Obtener el horario actual
            current_schedule = await self.schedule_repository.get_by_branch_and_day(branch_id, day_of_week)
            if not current_schedule:
                logger.warning(f"⚠️ Horario no encontrado para branch_id: {branch_id}, day_of_week: {day_of_week}")
                raise ScheduleNotFoundException(branch_id=branch_id, day_of_week=day_of_week.get_name())
            
            logger.info(f"✅ Horario actual encontrado: start_time={current_schedule.start_time}, end_time={current_schedule.end_time}")
            
            logger.info("📝 Obteniendo reservas afectadas...")
            # Obtener todas las reservas activas para esta sucursal y día
            affected_reservations = await self._get_affected_reservations(branch_id, day_of_week)
            logger.info(f"✅ Reservas afectadas encontradas: {len(affected_reservations)}")
            
            # Validar qué reservas se verían afectadas
            impacted_reservations = []
            safe_reservations = []
            
            logger.info("🔄 Analizando impacto en reservas...")
            for reservation in affected_reservations:
                if self._is_reservation_impacted(reservation, new_start_time, new_end_time):
                    impacted_reservations.append(reservation)
                    logger.info(f"⚠️ Reserva {reservation.id} será impactada")
                else:
                    safe_reservations.append(reservation)
                    logger.info(f"✅ Reserva {reservation.id} está segura")
            
            logger.info(f"📊 Análisis completado: {len(impacted_reservations)} impactadas, {len(safe_reservations)} seguras")
            
            # Crear DTO de análisis de impacto
            impact_analysis = ImpactAnalysisResponse(
                total_reservations=len(affected_reservations),
                impacted_reservations=len(impacted_reservations),
                safe_reservations=len(safe_reservations),
                impacted_reservation_ids=[r.id for r in impacted_reservations],
                safe_reservation_ids=[r.id for r in safe_reservations]
            )
            
            # Crear resultado usando el DTO
            result = ValidateScheduleChangesResult(
                branch_id=branch_id,
                day_of_week=day_of_week.value,
                day_name=DayOfWeek.get_name(day_of_week.value),
                current_schedule={
                    "start_time": current_schedule.start_time.strftime("%H:%M"),
                    "end_time": current_schedule.end_time.strftime("%H:%M"),
                    "interval_minutes": current_schedule.interval_minutes,
                    "is_active": current_schedule.is_active
                },
                proposed_changes={
                    "start_time": new_start_time,
                    "end_time": new_end_time,
                    "interval_minutes": new_interval_minutes,
                    "is_active": is_active
                },
                impact_analysis=impact_analysis,
                can_proceed=len(impacted_reservations) == 0,
                requires_rescheduling=len(impacted_reservations) > 0
            )
            
            logger.info(f"✅ Resultado preparado: can_proceed={result.can_proceed}, requires_rescheduling={result.requires_rescheduling}")
            return result
            
        except ScheduleNotFoundException as e:
            logger.warning(f"⚠️ Horario no encontrado en execute: {e.message}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado en execute: {str(e)}", exc_info=True)
            raise
    
    async def apply_schedule_changes(self, branch_id: int, day_of_week: DayOfWeek,
                                   new_start_time: str = None, new_end_time: str = None,
                                   new_interval_minutes: int = None, is_active: bool = None,
                                   auto_reschedule: bool = False) -> Dict[str, Any]:
        """Aplicar cambios de horario y actualizar reservas afectadas"""
        
        # Primero validar el impacto
        impact_analysis = await self.execute(branch_id, day_of_week, new_start_time, new_end_time, new_interval_minutes, is_active)
        
        if not impact_analysis.can_proceed and not auto_reschedule:
            return {
                "success": False,
                "message": "No se pueden aplicar los cambios sin reagendar las reservas afectadas",
                "impact_analysis": impact_analysis.dict()
            }
        
        # Obtener reservas afectadas
        affected_reservations = await self._get_affected_reservations(branch_id, day_of_week)
        impacted_reservations = []
        
        for reservation in affected_reservations:
            if self._is_reservation_impacted(reservation, new_start_time, new_end_time):
                impacted_reservations.append(reservation)
        
        # Marcar reservas afectadas para reagendamiento
        updated_reservations = []
        for reservation in impacted_reservations:
            reservation.mark_for_rescheduling()
            updated_reservation = await self.reservation_repository.update(reservation)
            if updated_reservation:
                updated_reservations.append(updated_reservation)
        
        return {
            "success": True,
            "message": f"Cambios aplicados. {len(updated_reservations)} reservas marcadas para reagendamiento",
            "impact_analysis": impact_analysis.dict(),
            "updated_reservations": len(updated_reservations)
        }
    
    async def _get_affected_reservations(self, branch_id: int, day_of_week: DayOfWeek) -> List[Reservation]:
        """Obtener reservas activas que podrían verse afectadas"""
        logger.info(f"🔄 Obteniendo reservas afectadas para branch_id: {branch_id}, day_of_week: {day_of_week}")
        
        all_reservations = []
        page = 1
        limit = 100  # Usar el límite máximo permitido
        
        while True:
            logger.info(f"📝 Obteniendo página {page} de reservas...")
            
            # Crear filtro para obtener reservas activas de esta sucursal
            filter_request = ReservationFilterRequest(
                branch_id=branch_id,
                status="PENDING,CONFIRMED",  # Solo reservas activas
                page=page,
                limit=limit
            )
            
            # Obtener reservas de esta página
            reservations, total = await self.reservation_repository.list(filter_request)
            logger.info(f"📊 Página {page}: {len(reservations)} reservas de {total} total")
            
            # Si no hay más reservas, terminar
            if not reservations:
                logger.info("✅ No hay más reservas para obtener")
                break
            
            # Agregar reservas de esta página
            all_reservations.extend(reservations)
            
            # Si ya obtuvimos todas las reservas, terminar
            if len(all_reservations) >= total:
                logger.info(f"✅ Todas las reservas obtenidas: {len(all_reservations)}")
                break
            
            # Ir a la siguiente página
            page += 1
        
        # Filtrar por día de la semana
        logger.info("🔄 Filtrando reservas por día de la semana...")
        affected_reservations = []
        for reservation in all_reservations:
            if reservation.reservation_date.isoweekday() == day_of_week.value:
                affected_reservations.append(reservation)
                logger.info(f"✅ Reserva {reservation.id} afectada (día {reservation.reservation_date.isoweekday()})")
        
        logger.info(f"📊 Reservas afectadas encontradas: {len(affected_reservations)} de {len(all_reservations)} total")
        return affected_reservations
    
    def _is_reservation_impacted(self, reservation: Reservation, new_start_time: str, new_end_time: str) -> bool:
        """Verificar si una reserva específica se ve afectada por los cambios"""
        if not new_start_time or not new_end_time:
            return False
        
        # Verificar si el horario de la reserva ya no está disponible
        reservation_start = reservation.start_time.time()
        reservation_end = reservation.end_time.time()
        new_start = datetime.strptime(new_start_time, "%H:%M").time()
        new_end = datetime.strptime(new_end_time, "%H:%M").time()
        
        # Verificar si hay solapamiento
        if (reservation_start >= new_end or reservation_end <= new_start):
            return True
        
        return False 