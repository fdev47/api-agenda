"""
Use case para obtener slots disponibles
"""
from datetime import datetime, date
from typing import List

from ...domain.entities.day_of_week import DayOfWeek
from ...domain.entities.time_slot import TimeSlot
from ...domain.entities.available_slots_response import AvailableSlotsResponse
from ...domain.dto.requests.schedule_requests import GetAvailableSlotsRequest
from ...domain.dto.responses.schedule_responses import AvailableSlotsResponse as AvailableSlotsResponseDTO, TimeSlotResponse
from ...domain.interfaces.schedule_repository import ScheduleRepository
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.exceptions.schedule_exceptions import (
    NoScheduleForDateException,
    PastDateException
)


class GetAvailableSlotsUseCase:
    """Caso de uso para obtener slots disponibles para una fecha"""
    
    def __init__(self, schedule_repository: ScheduleRepository):
        self.schedule_repository = schedule_repository
    
    async def execute(self, request: GetAvailableSlotsRequest) -> AvailableSlotsResponseDTO:
        """Ejecutar el caso de uso"""
        
        # Verificar que la fecha no sea en el pasado
        today = date.today()
        if request.schedule_date < today:
            raise PastDateException(str(request.schedule_date))
        
        # Obtener el día de la semana (1-7)
        day_of_week_number = request.schedule_date.isoweekday()
        day_of_week = DayOfWeek(day_of_week_number)
        
        # Obtener el horario configurado para ese día
        schedule = await self.schedule_repository.get_by_branch_and_day(
            request.branch_id, 
            day_of_week
        )
        
        if not schedule or not schedule.is_active:
            raise NoScheduleForDateException(
                request.branch_id,
                str(request.schedule_date),
                day_of_week.get_name()
            )
        
        # Generar slots disponibles
        available_slots = await self.schedule_repository.get_available_slots(
            request.branch_id,
            request.schedule_date
        )
        
        # Convertir a DTOs de respuesta
        slot_responses = [self.to_slot_response(slot) for slot in available_slots]
        
        # TODO: Obtener nombre de la sucursal desde location_service
        branch_name = f"Sucursal {request.branch_id}"
        
        return AvailableSlotsResponseDTO(
            branch_id=request.branch_id,
            branch_name=branch_name,
            date=datetime.combine(request.schedule_date, datetime.min.time()),
            day_of_week=day_of_week_number,
            day_name=day_of_week.get_name(),
            slots=slot_responses,
            total_slots=len(slot_responses),
            available_slots=len([slot for slot in slot_responses if slot.is_available])
        )
    
    def to_slot_response(self, slot: TimeSlot) -> TimeSlotResponse:
        """Convertir slot a DTO de respuesta"""
        return TimeSlotResponse(
            start_time=slot.start_time,
            end_time=slot.end_time,
            is_available=slot.is_available,
            reservation_id=slot.reservation_id,
            duration_minutes=slot.duration_minutes(),
            duration_hours=slot.duration_hours()
        ) 