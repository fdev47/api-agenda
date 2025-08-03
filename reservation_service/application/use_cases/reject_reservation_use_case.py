"""
Caso de uso para rechazar una reserva
"""
import logging
from datetime import datetime
from typing import Optional

from ...domain.entities.reservation import Reservation
from ...domain.entities.reservation_status import ReservationStatus
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.dto.requests.reject_reservation_request import RejectReservationRequest
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.exceptions.reservation_exceptions import (
    ReservationNotFoundException,
    ReservationStatusException
)

logger = logging.getLogger(__name__)


class RejectReservationUseCase:
    """Caso de uso para rechazar una reserva"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(self, reservation_id: int, reject_request: RejectReservationRequest) -> ReservationResponse:
        """
        Ejecutar el caso de uso para rechazar una reserva
        
        Args:
            reservation_id: ID de la reserva a rechazar
            reject_request: Datos del rechazo
            
        Returns:
            ReservationResponse: Reserva actualizada
            
        Raises:
            ReservationNotFoundException: Si la reserva no existe
            ReservationStatusException: Si la reserva ya está cancelada o completada
        """
        logger.info(f"🚀 Ejecutando RejectReservationUseCase para reserva {reservation_id}")
        
        # 1. Obtener la reserva
        reservation = await self.reservation_repository.get_by_id(reservation_id)
        if not reservation:
            logger.warning(f"⚠️ Reserva {reservation_id} no encontrada")
            raise ReservationNotFoundException(f"Reserva con ID {reservation_id} no encontrada")
        
        # 2. Validar que la reserva pueda ser rechazada
        if reservation.status == ReservationStatus.CANCELLED:
            logger.warning(f"⚠️ Reserva {reservation_id} ya está cancelada")
            raise ReservationStatusException("La reserva ya está cancelada")
        
        if reservation.status == ReservationStatus.COMPLETED:
            logger.warning(f"⚠️ Reserva {reservation_id} ya está completada")
            raise ReservationStatusException("No se puede rechazar una reserva completada")
        
        # 3. Crear el closing_summary con los datos del rechazo
        closing_summary = {
            "action": "rejected",
            "user_id": reject_request.user_id,
            "user_name": reject_request.user_name,
            "date": reject_request.date.isoformat(),
            "reason": reject_request.reason,
            "comment": reject_request.comment
        }
        
        # 4. Actualizar la reserva
        reservation.closing_summary = closing_summary
        reservation.status = ReservationStatus.CANCELLED
        reservation.updated_at = datetime.utcnow()
        
        # 5. Guardar en el repositorio
        updated_reservation = await self.reservation_repository.update(reservation)
        
        logger.info(f"✅ Reserva {reservation_id} rechazada exitosamente")
        
        # 6. Convertir a DTO de respuesta
        return ReservationResponse(
            id=updated_reservation.id,
            user_id=updated_reservation.user_id,
            customer_id=updated_reservation.customer_id,
            branch_data=updated_reservation.branch_data,
            sector_data=updated_reservation.sector_data,
            customer_data=updated_reservation.customer_data,
            unloading_time_minutes=updated_reservation.unloading_time_minutes,
            unloading_time_hours=updated_reservation.get_total_unloading_time_hours(),
            reason=updated_reservation.reason,
            cargo_type=updated_reservation.cargo_type,
            order_numbers=updated_reservation.order_numbers,
            reservation_date=updated_reservation.reservation_date,
            start_time=updated_reservation.start_time,
            end_time=updated_reservation.end_time,
            status=updated_reservation.status.value,
            notes=updated_reservation.notes,
            closing_summary=updated_reservation.closing_summary,
            created_at=updated_reservation.created_at,
            updated_at=updated_reservation.updated_at
        ) 