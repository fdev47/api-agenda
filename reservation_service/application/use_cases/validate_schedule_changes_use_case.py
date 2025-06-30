from typing import List, Dict, Any
from datetime import datetime

from ...domain.interfaces import ScheduleRepository, ReservationRepository
from ...domain.entities.schedule import DayOfWeek
from ...domain.entities.reservation import Reservation, ReservationStatus
from ...domain.dto.requests.reservation_requests import ReservationFilterRequest
from ...domain.exceptions.schedule_exceptions import ScheduleNotFoundException


class ValidateScheduleChangesUseCase:
    """Caso de uso para validar y actualizar reservas afectadas por cambios de horario"""
    
    def __init__(self, schedule_repository: ScheduleRepository, reservation_repository: ReservationRepository):
        self.schedule_repository = schedule_repository
        self.reservation_repository = reservation_repository
    
    async def execute(self, branch_id: int, day_of_week: DayOfWeek, 
                     new_start_time: str = None, new_end_time: str = None,
                     new_interval_minutes: int = None, is_active: bool = None) -> Dict[str, Any]:
        """Ejecutar validación de cambios de horario"""
        
        # Obtener el horario actual
        current_schedule = await self.schedule_repository.get_by_branch_and_day(branch_id, day_of_week)
        if not current_schedule:
            raise ScheduleNotFoundException(branch_id=branch_id, day_of_week=day_of_week.get_name())
        
        # Obtener todas las reservas activas para esta sucursal y día
        affected_reservations = await self._get_affected_reservations(branch_id, day_of_week)
        
        # Validar qué reservas se verían afectadas
        impacted_reservations = []
        safe_reservations = []
        
        for reservation in affected_reservations:
            if self._is_reservation_impacted(reservation, new_start_time, new_end_time):
                impacted_reservations.append(reservation)
            else:
                safe_reservations.append(reservation)
        
        # Preparar respuesta
        result = {
            "branch_id": branch_id,
            "day_of_week": day_of_week.value,
            "day_name": day_of_week.get_name(),
            "current_schedule": {
                "start_time": current_schedule.start_time.strftime("%H:%M"),
                "end_time": current_schedule.end_time.strftime("%H:%M"),
                "interval_minutes": current_schedule.interval_minutes,
                "is_active": current_schedule.is_active
            },
            "proposed_changes": {
                "start_time": new_start_time,
                "end_time": new_end_time,
                "interval_minutes": new_interval_minutes,
                "is_active": is_active
            },
            "impact_analysis": {
                "total_reservations": len(affected_reservations),
                "impacted_reservations": len(impacted_reservations),
                "safe_reservations": len(safe_reservations),
                "impacted_reservation_ids": [r.id for r in impacted_reservations],
                "safe_reservation_ids": [r.id for r in safe_reservations]
            },
            "can_proceed": len(impacted_reservations) == 0,
            "requires_rescheduling": len(impacted_reservations) > 0
        }
        
        return result
    
    async def apply_schedule_changes(self, branch_id: int, day_of_week: DayOfWeek,
                                   new_start_time: str = None, new_end_time: str = None,
                                   new_interval_minutes: int = None, is_active: bool = None,
                                   auto_reschedule: bool = False) -> Dict[str, Any]:
        """Aplicar cambios de horario y actualizar reservas afectadas"""
        
        # Primero validar el impacto
        impact_analysis = await self.execute(branch_id, day_of_week, new_start_time, new_end_time, new_interval_minutes, is_active)
        
        if not impact_analysis["can_proceed"] and not auto_reschedule:
            return {
                "success": False,
                "message": "No se pueden aplicar los cambios sin reagendar las reservas afectadas",
                "impact_analysis": impact_analysis
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
            "impact_analysis": impact_analysis,
            "updated_reservations": len(updated_reservations)
        }
    
    async def _get_affected_reservations(self, branch_id: int, day_of_week: DayOfWeek) -> List[Reservation]:
        """Obtener reservas activas que podrían verse afectadas"""
        # Crear filtro para obtener reservas activas de esta sucursal
        filter_request = ReservationFilterRequest(
            branch_id=branch_id,
            status="PENDING,CONFIRMED",  # Solo reservas activas
            limit=1000  # Obtener todas las reservas activas
        )
        
        # Obtener reservas
        reservations, _ = await self.reservation_repository.list(filter_request)
        
        # Filtrar por día de la semana
        affected_reservations = []
        for reservation in reservations:
            if reservation.reservation_date.isoweekday() == day_of_week.value:
                affected_reservations.append(reservation)
        
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