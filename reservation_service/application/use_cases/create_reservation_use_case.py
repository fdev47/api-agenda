"""
Use case para crear una reserva
"""
from typing import Optional
from datetime import datetime
from typing import List

from ...domain.entities.reservation import Reservation
from ...domain.entities.order_number import OrderNumber
from ...domain.entities.customer_data import CustomerData
from ...domain.entities.branch_data import BranchData
from ...domain.entities.sector_data import SectorData
from ...domain.entities.reservation_status import ReservationStatus
from ...domain.dto.requests.create_reservation_request import CreateReservationRequest
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.interfaces.schedule_repository import ScheduleRepository
from ...domain.exceptions.reservation_exceptions import (
    ReservationAlreadyExistsException,
    ReservationValidationException
)


class CreateReservationUseCase:
    """Caso de uso para crear una nueva reserva"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(self, request: CreateReservationRequest) -> ReservationResponse:
        """Ejecutar el caso de uso"""
        
        # Convertir DTOs de request a entidades de dominio
        customer_data = CustomerData(
            customer_id=request.customer_data.customer_id,
            id=request.customer_data.id,
            auth_uid=request.customer_data.auth_uid,
            ruc=request.customer_data.ruc,
            company_name=request.customer_data.company_name,
            email=request.customer_data.email,
            username=request.customer_data.username,
            phone=request.customer_data.phone,
            cellphone_number=request.customer_data.cellphone_number,
            cellphone_country_code=request.customer_data.cellphone_country_code,
            address_id=request.customer_data.address_id,
            is_active=request.customer_data.is_active
        )
        
        branch_data = BranchData(
            branch_id=request.branch_data.branch_id,
            name=request.branch_data.name,
            code=request.branch_data.code,
            address=request.branch_data.address,
            country_id=request.branch_data.country_id,
            country_name=request.branch_data.country_name,
            state_id=request.branch_data.state_id,
            state_name=request.branch_data.state_name,
            city_id=request.branch_data.city_id,
            city_name=request.branch_data.city_name
        )
        
        sector_data = SectorData(
            sector_id=request.sector_data.sector_id,
            name=request.sector_data.name,
            description=request.sector_data.description,
            sector_type_id=request.sector_data.sector_type_id,
            sector_type_name=request.sector_data.sector_type_name,
            measurement_unit=request.sector_data.measurement_unit
        )
        
        # Convertir números de pedido
        order_numbers = [
            OrderNumber(code=order.code, description=order.description)
            for order in request.order_numbers
        ]
        
        # Crear la entidad de reserva
        reservation = Reservation(
            user_id=request.user_id,
            customer_id=request.customer_id,
            branch_data=branch_data,
            sector_data=sector_data,
            customer_data=customer_data,
            unloading_time_minutes=request.unloading_time_minutes,
            reason=request.reason,
            order_numbers=order_numbers,
            reservation_date=request.reservation_date,
            start_time=request.start_time,
            end_time=request.end_time,
            notes=request.notes,
            status=ReservationStatus.PENDING
        )
        
        # Verificar conflictos de horario
        conflicts = await self.reservation_repository.check_conflicts(
            branch_id=reservation.get_branch_id(),
            sector_id=reservation.get_sector_id(),
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            exclude_reservation_id=None
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
        
        # Guardar la reserva
        saved_reservation = await self.reservation_repository.create(reservation)
        
        # Convertir a DTO de respuesta
        return self.to_response(saved_reservation)
    
    def to_response(self, reservation: Reservation) -> ReservationResponse:
        """Convertir entidad a DTO de respuesta"""
        from ...domain.dto.responses.reservation_responses import (
            CustomerDataResponse, BranchDataResponse, SectorDataResponse, OrderNumberResponse
        )
        
        # Convertir datos del cliente
        customer_response = CustomerDataResponse(
            customer_id=reservation.customer_data.customer_id,
            id=reservation.customer_data.id,
            auth_uid=reservation.customer_data.auth_uid,
            ruc=reservation.customer_data.ruc,
            company_name=reservation.customer_data.company_name,
            email=reservation.customer_data.email,
            username=reservation.customer_data.username,
            phone=reservation.customer_data.phone,
            cellphone_number=reservation.customer_data.cellphone_number,
            cellphone_country_code=reservation.customer_data.cellphone_country_code,
            address_id=reservation.customer_data.address_id,
            is_active=reservation.customer_data.is_active
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
            measurement_unit=reservation.sector_data.measurement_unit
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