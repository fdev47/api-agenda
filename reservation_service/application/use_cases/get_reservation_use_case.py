"""
Use case para obtener una reserva
"""
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.exceptions.reservation_exceptions import ReservationNotFoundException


class GetReservationUseCase:
    """Caso de uso para obtener una reserva por ID"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(self, reservation_id: int) -> ReservationResponse:
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
    
    def to_response(self, reservation) -> ReservationResponse:
        """Convertir entidad a DTO de respuesta"""
        from ...domain.dto.responses.reservation_responses import (
            CustomerDataResponse, BranchDataResponse, SectorDataResponse, OrderNumberResponse
        )
        
        # Convertir datos del cliente
        customer_response = CustomerDataResponse(
            customer_id=reservation.customer_data.customer_id,
            ruc=reservation.customer_data.ruc,
            company_name=reservation.customer_data.company_name,
            phone_number=reservation.customer_data.phone_number
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