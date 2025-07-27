"""
Use case para listar reservas
"""
from typing import List
from ...domain.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.dto.responses.reservation_list_response import ReservationListResponse
from ...domain.dto.responses.reservation_summary_response import ReservationSummaryResponse
from ...domain.interfaces.reservation_repository import ReservationRepository


class ListReservationsUseCase:
    """Caso de uso para listar reservas con filtros y paginación"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(self, request: ReservationFilterRequest) -> ReservationListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener reservas con filtros
        reservations, total = await self.reservation_repository.list_with_filters(
            user_id=request.user_id,
            customer_id=request.customer_id,
            branch_id=request.branch_id,
            sector_id=request.sector_id,
            customer_ruc=request.customer_ruc,
            company_name=request.company_name,
            reservation_date_from=request.reservation_date_from,
            reservation_date_to=request.reservation_date_to,
            status=request.status,
            order_code=request.order_code,
            offset=request.offset,
            limit=request.limit
        )
        
        # Convertir a DTOs de respuesta
        reservation_responses = [self.to_response(reservation) for reservation in reservations]
        
        # Calcular páginas
        pages = (total + request.limit - 1) // request.limit
        
        return ReservationListResponse(
            items=reservation_responses,
            total=total,
            page=request.page,
            size=request.limit,
            pages=pages
        )
    
    def to_response(self, reservation) -> ReservationSummaryResponse:
        """Convertir entidad a DTO de respuesta resumida"""
        return ReservationSummaryResponse(
            id=reservation.id,
            customer_company_name=reservation.customer_data.company_name,
            branch_id=reservation.branch_data.branch_id,
            branch_name=reservation.branch_data.name,
            sector_id=reservation.sector_data.sector_id,
            sector_name=reservation.sector_data.name,
            reservation_date=reservation.reservation_date,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            status=reservation.status.value,
            order_count=len(reservation.order_numbers),
            unloading_time_hours=reservation.get_total_unloading_time_hours()
        ) 