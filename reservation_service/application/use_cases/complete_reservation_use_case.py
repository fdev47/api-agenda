"""
Caso de uso para completar una reserva
"""
import logging
from datetime import datetime
from typing import Optional

from ...domain.entities.reservation import Reservation
from ...domain.entities.reservation_status import ReservationStatus
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.dto.requests.complete_reservation_request import CompleteReservationRequest
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.dto.responses.branch_data_response import BranchDataResponse
from ...domain.dto.responses.sector_data_response import SectorDataResponse
from ...domain.dto.responses.customer_data_response import CustomerDataResponse
from ...domain.dto.responses.order_number_response import OrderNumberResponse
from ...domain.exceptions.reservation_exceptions import (
    ReservationNotFoundException,
    ReservationStatusException
)

logger = logging.getLogger(__name__)

class CompleteReservationUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    async def execute(self, reservation_id: int, complete_request: CompleteReservationRequest) -> ReservationResponse:
        logger.info(f"🚀 Ejecutando CompleteReservationUseCase para reserva {reservation_id}")
        
        # Obtener la reserva
        reservation = await self.reservation_repository.get_by_id(reservation_id)
        if not reservation:
            logger.warning(f"⚠️ Reserva {reservation_id} no encontrada")
            raise ReservationNotFoundException(f"Reserva con ID {reservation_id} no encontrada")

        # Validar que la reserva no esté ya completada
        if reservation.status == ReservationStatus.COMPLETED:
            logger.warning(f"⚠️ Reserva {reservation_id} ya está completada")
            raise ReservationStatusException("La reserva ya está completada")

        # Validar que la reserva no esté cancelada
        if reservation.status == ReservationStatus.CANCELLED:
            logger.warning(f"⚠️ Reserva {reservation_id} está cancelada")
            raise ReservationStatusException("No se puede completar una reserva cancelada")

        # Crear el closing_summary con los datos del completado
        closing_summary = {
            "action": "completed",
            "user_id": complete_request.user_id,
            "user_name": complete_request.user_name,
            "date": complete_request.date.isoformat(),
            "download_time": complete_request.download_time,
            "success_code": complete_request.success_code,
            "comment": complete_request.comment
        }

        # Actualizar la reserva
        reservation.closing_summary = closing_summary
        reservation.status = ReservationStatus.COMPLETED
        reservation.updated_at = datetime.utcnow()

        updated_reservation = await self.reservation_repository.update(reservation)

        logger.info(f"✅ Reserva {reservation_id} completada exitosamente")

        return ReservationResponse(
            id=updated_reservation.id,
            user_id=updated_reservation.user_id,
            customer_id=updated_reservation.customer_id,
            branch_data=BranchDataResponse(
                branch_id=updated_reservation.branch_data.branch_id,
                name=updated_reservation.branch_data.name,
                code=updated_reservation.branch_data.code,
                address=updated_reservation.branch_data.address,
                country_id=updated_reservation.branch_data.country_id,
                country_name=updated_reservation.branch_data.country_name,
                state_id=updated_reservation.branch_data.state_id,
                state_name=updated_reservation.branch_data.state_name,
                city_id=updated_reservation.branch_data.city_id,
                city_name=updated_reservation.branch_data.city_name,
                ramp_id=updated_reservation.branch_data.ramp_id,
                ramp_name=updated_reservation.branch_data.ramp_name
            ),
            sector_data=SectorDataResponse(
                sector_id=updated_reservation.sector_data.sector_id,
                name=updated_reservation.sector_data.name,
                description=updated_reservation.sector_data.description,
                sector_type_id=updated_reservation.sector_data.sector_type_id,
                sector_type_name=updated_reservation.sector_data.sector_type_name,
                capacity=updated_reservation.sector_data.capacity,
                measurement_unit_id=updated_reservation.sector_data.measurement_unit_id,
                measurement_unit_name=updated_reservation.sector_data.measurement_unit_name
            ),
            customer_data=CustomerDataResponse(
                customer_id=updated_reservation.customer_data.customer_id,
                id=updated_reservation.customer_data.id,
                auth_uid=updated_reservation.customer_data.auth_uid,
                ruc=updated_reservation.customer_data.ruc,
                company_name=updated_reservation.customer_data.company_name,
                email=updated_reservation.customer_data.email,
                username=updated_reservation.customer_data.username,
                phone=updated_reservation.customer_data.phone,
                cellphone_number=updated_reservation.customer_data.cellphone_number,
                cellphone_country_code=updated_reservation.customer_data.cellphone_country_code,
                address_id=updated_reservation.customer_data.address_id,
                is_active=updated_reservation.customer_data.is_active
            ),
            unloading_time_minutes=updated_reservation.unloading_time_minutes,
            unloading_time_hours=updated_reservation.get_total_unloading_time_hours(),
            reason=updated_reservation.reason,
            cargo_type=updated_reservation.cargo_type,
            order_numbers=[
                OrderNumberResponse(
                    code=order.code,
                    description=order.description
                ) for order in updated_reservation.order_numbers
            ],
            reservation_date=updated_reservation.reservation_date,
            start_time=updated_reservation.start_time,
            end_time=updated_reservation.end_time,
            status=updated_reservation.status.value,
            notes=updated_reservation.notes,
            created_at=updated_reservation.created_at,
            updated_at=updated_reservation.updated_at
        ) 