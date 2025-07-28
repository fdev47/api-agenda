"""
Use case para listar reservas
"""
from typing import List
from ...domain.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.dto.responses.reservation_summary_list_response import ReservationSummaryListResponse
from ...domain.dto.responses.reservation_summary_response import ReservationSummaryResponse
from ...domain.interfaces.reservation_repository import ReservationRepository


class ListReservationsUseCase:
    """Caso de uso para listar reservas con filtros y paginación"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(self, request: ReservationFilterRequest) -> ReservationSummaryListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener reservas con filtros
        reservations, total = await self.reservation_repository.list(request)
        
        # Convertir a DTOs de respuesta
        reservation_responses = [self.to_response(reservation) for reservation in reservations]
        
        # Calcular páginas
        pages = (total + request.limit - 1) // request.limit
        
        return ReservationSummaryListResponse(
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
            customer_name=reservation.customer_data.company_name,
            customer_email=reservation.customer_data.email,
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