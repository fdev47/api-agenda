"""
Use case para listar reservas
"""
from typing import List
from ...domain.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.dto.responses.reservation_list_response import ReservationListResponse
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.interfaces.main_reservation_repository import MainReservationRepository


class ListReservationsUseCase:
    """Caso de uso para listar reservas con filtros y paginación"""
    
    def __init__(
        self, 
        reservation_repository: ReservationRepository,
        main_reservation_repository: MainReservationRepository
    ):
        self.reservation_repository = reservation_repository
        self.main_reservation_repository = main_reservation_repository
    
    async def execute(self, request: ReservationFilterRequest) -> ReservationListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener reservas con filtros
        reservations, total = await self.reservation_repository.list(request)
        
        # Convertir a DTOs de respuesta
        reservation_responses = []
        for reservation in reservations:
            # Obtener las main_reservations asociadas
            main_reservations, _ = await self.main_reservation_repository.list(
                reservation_id=reservation.id
            )
            reservation_response = await self.to_response(reservation, main_reservations)
            reservation_responses.append(reservation_response)
        
        # Calcular páginas
        pages = (total + request.limit - 1) // request.limit
        
        return ReservationListResponse(
            items=reservation_responses,
            total=total,
            page=request.page,
            size=request.limit,
            pages=pages
        )
    
    async def to_response(self, reservation, main_reservations: List) -> ReservationResponse:
        """Convertir entidad a DTO de respuesta completa"""
        from ...domain.dto.responses.customer_data_response import CustomerDataResponse
        from ...domain.dto.responses.main_reservation_response import MainReservationResponse
        from ...domain.dto.responses.sector_data_response import SectorDataResponse
        
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
        
        # Convertir main_reservations a DTOs
        main_reservations_response = []
        for main_res in main_reservations:
            sector_data_response = SectorDataResponse(
                sector_id=main_res.sector_data.sector_id,
                name=main_res.sector_data.name,
                description=main_res.sector_data.description,
                sector_type_id=main_res.sector_data.sector_type_id,
                sector_type_name=main_res.sector_data.sector_type_name,
                capacity=main_res.sector_data.capacity,
                measurement_unit_id=main_res.sector_data.measurement_unit_id,
                measurement_unit_name=main_res.sector_data.measurement_unit_name,
                pallet_count=main_res.sector_data.pallet_count,
                granel_count=main_res.sector_data.granel_count,
                boxes_count=main_res.sector_data.boxes_count,
                order_numbers=main_res.sector_data.order_numbers,
                ramp_id=main_res.sector_data.ramp_id,
                ramp_name=main_res.sector_data.ramp_name
            )
            
            main_res_response = MainReservationResponse(
                id=main_res.id,
                sector_id=main_res.sector_id,
                reservation_id=main_res.reservation_id,
                sector_data=sector_data_response,
                reservation_date=main_res.reservation_date,
                start_time=main_res.start_time,
                end_time=main_res.end_time,
                created_at=main_res.created_at,
                updated_at=main_res.updated_at
            )
            main_reservations_response.append(main_res_response)
        
        return ReservationResponse(
            id=reservation.id,
            user_id=reservation.user_id,
            customer_id=reservation.customer_id,
            branch_id=reservation.branch_data.branch_id,
            main_reservations=main_reservations_response,
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