"""
Use case para actualizar una reserva
"""
from datetime import datetime
from typing import List, Optional

from ...domain.entities.order_number import OrderNumber
from ...domain.dto.requests.update_reservation_request import UpdateReservationRequest
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.entities.reservation import Reservation
from ...domain.exceptions.reservation_exceptions import (
    ReservationNotFoundException,
    ReservationAlreadyExistsException,
    ReservationStatusException
)


class UpdateReservationUseCase:
    """Caso de uso para actualizar una reserva"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(self, reservation_id: int, request: UpdateReservationRequest) -> ReservationResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener la reserva existente
        reservation = await self.reservation_repository.get_by_id(reservation_id)
        
        if not reservation:
            raise ReservationNotFoundException(
                f"Reserva con ID {reservation_id} no encontrada",
                reservation_id=reservation_id
            )
        
        # Verificar que la reserva se pueda actualizar
        if reservation.is_cancelled():
            raise ReservationStatusException(
                f"No se puede actualizar una reserva cancelada",
                current_status=reservation.status.value
            )
        
        if reservation.is_completed():
            raise ReservationStatusException(
                f"No se puede actualizar una reserva completada",
                current_status=reservation.status.value
            )
        
        # Actualizar campos si están presentes en el request
        if request.unloading_time_minutes is not None:
            reservation.unloading_time_minutes = request.unloading_time_minutes
        
        if request.reason is not None:
            reservation.reason = request.reason
        
        if request.notes is not None:
            reservation.notes = request.notes
        
        if request.order_numbers is not None:
            # Convertir números de pedido
            order_numbers = [
                OrderNumber(code=order.code, description=order.description)
                for order in request.order_numbers
            ]
            reservation.order_numbers = order_numbers
        
        # Actualizar horarios si están presentes
        if request.start_time is not None:
            reservation.start_time = request.start_time
        
        if request.end_time is not None:
            reservation.end_time = request.end_time
        
        # Verificar conflictos de horario si se actualizaron los horarios
        if request.start_time is not None or request.end_time is not None:
            conflicts = await self.reservation_repository.check_conflicts(
                branch_id=reservation.get_branch_id(),
                sector_id=reservation.get_sector_id(),
                start_time=reservation.start_time,
                end_time=reservation.end_time,
                exclude_reservation_id=reservation_id
            )
            
            if conflicts:
                raise ReservationAlreadyExistsException(
                    f"Ya existe una reserva en el horario {reservation.start_time.strftime('%H:%M')}-{reservation.end_time.strftime('%H:%M')} "
                    f"para la sucursal {reservation.get_branch_id()} y sector {reservation.get_sector_id()}",
                    branch_id=reservation.get_branch_id(),
                    sector_id=reservation.get_sector_id(),
                    start_time=reservation.start_time,
                    end_time=reservation.end_time
                )
        
        # Actualizar timestamp
        reservation.updated_at = datetime.utcnow()
        
        # Guardar la reserva actualizada
        updated_reservation = await self.reservation_repository.update(reservation)
        
        # Convertir a DTO de respuesta
        return self.to_response(updated_reservation)
    
    def to_response(self, reservation: Reservation) -> ReservationResponse:
        """Convertir entidad a DTO de respuesta"""
        from ...domain.dto.responses.customer_data_response import CustomerDataResponse
        from ...domain.dto.responses.branch_data_response import BranchDataResponse
        from ...domain.dto.responses.sector_data_response import SectorDataResponse
        from ...domain.dto.responses.order_number_response import OrderNumberResponse
        
        # Convertir datos del cliente
        customer_response = CustomerDataResponse(
            customer_id=reservation.customer_data.customer_id,
            name=reservation.customer_data.name,
            email=reservation.customer_data.email,
            phone=reservation.customer_data.phone
        )
        
        # Convertir datos de la sucursal
        branch_response = BranchDataResponse(
            branch_id=reservation.branch_data.branch_id,
            name=reservation.branch_data.name,
            code=reservation.branch_data.code,
            address=reservation.branch_data.address,
            country_id=reservation.branch_data.country_id,
            country_name=reservation.branch_data.country_name,
            state_id=reservation.branch_data.state_id,
            state_name=reservation.branch_data.state_name,
            city_id=reservation.branch_data.city_id,
            city_name=reservation.branch_data.city_name
        )
        
        # Convertir datos del sector
        sector_response = SectorDataResponse(
            sector_id=reservation.sector_data.sector_id,
            name=reservation.sector_data.name,
            description=reservation.sector_data.description,
            sector_type_id=reservation.sector_data.sector_type_id,
            sector_type_name=reservation.sector_data.sector_type_name,
            capacity=reservation.sector_data.capacity,
            measurement_unit_id=reservation.sector_data.measurement_unit_id,
            measurement_unit_name=reservation.sector_data.measurement_unit_name
        )
        
        # Convertir números de pedido
        order_responses = [
            OrderNumberResponse(code=order.code, description=order.description)
            for order in reservation.order_numbers
        ]
        
        return ReservationResponse(
            id=reservation.id,
            user_id=reservation.user_id,
            customer_id=reservation.customer_id,
            branch_data=branch_response,
            sector_data=sector_response,
            customer_data=customer_response,
            unloading_time_minutes=reservation.unloading_time_minutes,
            unloading_time_hours=reservation.get_total_unloading_time_hours(),
            reason=reservation.reason,
            order_numbers=order_responses,
            reservation_date=reservation.reservation_date,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            status=reservation.status.value,
            notes=reservation.notes,
            created_at=reservation.created_at,
            updated_at=reservation.updated_at
        ) 