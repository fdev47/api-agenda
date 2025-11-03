"""
Use case para listar reservas
"""
from typing import List
from ...domain.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.dto.responses.reservation_list_response import ReservationListResponse
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.interfaces.reservation_repository import ReservationRepository


class ListReservationsUseCase:
    """Caso de uso para listar reservas con filtros y paginación"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(self, request: ReservationFilterRequest) -> ReservationListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener reservas con filtros
        reservations, total = await self.reservation_repository.list(request)
        
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
    
    def to_response(self, reservation) -> ReservationResponse:
        """Convertir entidad a DTO de respuesta completa"""
        from ...domain.dto.responses.customer_data_response import CustomerDataResponse
        from ...domain.dto.responses.branch_data_response import BranchDataResponse
        from ...domain.dto.responses.sector_data_response import SectorDataResponse
        from ...domain.dto.responses.order_number_response import OrderNumberResponse
        
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
        
        return ReservationResponse(
            id=reservation.id,
            user_id=reservation.user_id,
            customer_id=reservation.customer_id,
            branch_data=branch_response,
            sector_id=reservation.sector_data.sector_id,
            customer_data=customer_response,
            unloading_time_minutes=reservation.unloading_time_minutes,
            unloading_time_hours=reservation.get_total_unloading_time_hours(),
            reason=reservation.reason,
            cargo_type=reservation.cargo_type,
            reservation_date=reservation.reservation_date,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            status=reservation.status.value,
            notes=reservation.notes,
            created_at=reservation.created_at,
            updated_at=reservation.updated_at
        ) 