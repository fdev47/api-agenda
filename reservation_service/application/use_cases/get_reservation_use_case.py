"""
Use case para obtener una reserva
"""
from ...domain.dto.responses.reservation_detail_response import ReservationDetailResponse
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.exceptions.reservation_exceptions import ReservationNotFoundException


class GetReservationUseCase:
    """Caso de uso para obtener una reserva por ID"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(self, reservation_id: int) -> ReservationDetailResponse:
        """Ejecutar el caso de uso"""
        
        # Buscar la reserva
        reservation = await self.reservation_repository.get_by_id(reservation_id)
        
        if not reservation:
            raise ReservationNotFoundException(
                f"Reserva con ID {reservation_id} no encontrada",
                reservation_id=reservation_id
            )
        
        # Convertir a DTO de respuesta
        return self.to_response(reservation)
    
    def to_response(self, reservation) -> ReservationDetailResponse:
        """Convertir entidad a DTO de respuesta"""
        from ...domain.dto.responses.reservation_responses import (
            CustomerDataResponse, BranchDataResponse, SectorDataResponse, OrderNumberResponse
        )
        
        # Convertir datos del cliente
        customer_response = CustomerDataResponse(
            customer_id=reservation.customer_data.customer_id,
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
            measurement_unit=reservation.sector_data.measurement_unit
        )
        
        # Convertir números de pedido
        order_responses = [
            OrderNumberResponse(code=order.code, description=order.description)
            for order in reservation.order_numbers
        ]
        
        # Preparar datos para el closing_summary
        closing_summary_raw = reservation.closing_summary if reservation.closing_summary else None
        
        return ReservationDetailResponse(
            id=reservation.id,
            user_id=reservation.user_id,
            customer_id=reservation.customer_id,
            branch_data=reservation.branch_data.__dict__,
            sector_data=reservation.sector_data.__dict__,
            customer_data=reservation.customer_data.__dict__,
            merchandise_description=reservation.reason,
            merchandise_quantity=reservation.unloading_time_minutes,
            merchandise_unit=reservation.sector_data.measurement_unit_name,
            cargo_type=reservation.cargo_type,
            schedule_date=reservation.reservation_date.isoformat() if reservation.reservation_date else None,
            schedule_start_time=reservation.start_time.strftime("%H:%M") if reservation.start_time else None,
            schedule_end_time=reservation.end_time.strftime("%H:%M") if reservation.end_time else None,
            status=reservation.status.value,
            special_requirements=reservation.notes,
            order_numbers=[order.code for order in reservation.order_numbers],
            created_at=reservation.created_at.isoformat() if reservation.created_at else None,
            updated_at=reservation.updated_at.isoformat() if reservation.updated_at else None,
            closing_summary=closing_summary_raw
        ) 