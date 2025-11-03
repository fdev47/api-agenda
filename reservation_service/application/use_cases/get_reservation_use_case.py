"""
Use case para obtener una reserva
"""
import logging
from ...domain.dto.responses.reservation_detail_response import ReservationDetailResponse
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.interfaces.main_reservation_repository import MainReservationRepository
from ...domain.exceptions.reservation_exceptions import ReservationNotFoundException

logger = logging.getLogger(__name__)


class GetReservationUseCase:
    """Caso de uso para obtener una reserva por ID"""
    
    def __init__(
        self, 
        reservation_repository: ReservationRepository,
        main_reservation_repository: MainReservationRepository
    ):
        self.reservation_repository = reservation_repository
        self.main_reservation_repository = main_reservation_repository
    
    async def execute(self, reservation_id: int) -> ReservationDetailResponse:
        """Ejecutar el caso de uso"""
        
        try:
            logger.info(f"🔍 Buscando reserva con ID: {reservation_id}")
            
            # Buscar la reserva
            reservation = await self.reservation_repository.get_by_id(reservation_id)
            
            if not reservation:
                logger.warning(f"⚠️ Reserva no encontrada: {reservation_id}")
                raise ReservationNotFoundException(
                    f"Reserva con ID {reservation_id} no encontrada",
                    reservation_id=reservation_id
                )
            
            logger.info(f"✅ Reserva encontrada: {reservation.id}")
            
            # Obtener las main_reservations asociadas
            logger.info(f"🔍 Buscando main_reservations para reservation_id: {reservation_id}")
            main_reservations, _ = await self.main_reservation_repository.list(
                reservation_id=reservation_id
            )
            logger.info(f"✅ Se encontraron {len(main_reservations)} main_reservations")
            
            logger.info("🔄 Convirtiendo a DTO de respuesta...")
            
            # Convertir a DTO de respuesta
            result = await self.to_response(reservation, main_reservations)
            logger.info("✅ Conversión completada exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error en GetReservationUseCase.execute(): {str(e)}", exc_info=True)
            raise
    
    async def to_response(self, reservation, main_reservations) -> ReservationDetailResponse:
        """Convertir entidad a DTO de respuesta"""
        try:
            logger.info("🔄 Iniciando conversión a DTO...")
            
            from ...domain.dto.responses.customer_data_response import CustomerDataResponse
            from ...domain.dto.responses.main_reservation_response import MainReservationResponse
            from ...domain.dto.responses.sector_data_response import SectorDataResponse
            from ...domain.dto.responses.branch_data_response import BranchDataResponse
            
            logger.info("✅ Imports completados")
            
            # Convertir datos del cliente
            logger.info("🔄 Convirtiendo datos del cliente...")
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
            logger.info("✅ CustomerDataResponse creado")
            
            # Convertir datos de la sucursal
            logger.info("🔄 Convirtiendo datos de la sucursal...")
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
            logger.info("✅ BranchDataResponse creado")
            
            # Convertir main_reservations a DTOs
            logger.info("🔄 Convirtiendo main_reservations...")
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
            logger.info("✅ MainReservations convertidas")
            
            # Crear ReservationDetailResponse
            logger.info("🔄 Creando ReservationDetailResponse...")
            
            # Debug: Log del closing_summary
            logger.info(f"🔍 Closing summary de la reserva: {reservation.closing_summary}")
            
            # Determinar el tipo de closing_summary basado en el status
            from ...domain.dto.responses.reservation_detail_response import ClosingSummaryType
            if reservation.status.value == "COMPLETED":
                closing_summary_type = ClosingSummaryType.COMPLETED
            elif reservation.status.value == "CANCELLED":
                closing_summary_type = ClosingSummaryType.REJECTED
            else:
                closing_summary_type = ClosingSummaryType.NONE
            
            logger.info(f"🔍 Closing summary type determinado: {closing_summary_type}")
            
            result = ReservationDetailResponse(
                id=reservation.id,
                user_id=reservation.user_id,
                customer_id=reservation.customer_id,
                branch_data=branch_response,
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
                updated_at=reservation.updated_at,
                closing_summary_type=closing_summary_type,
                closing_summary=reservation.closing_summary
            )
            logger.info("✅ ReservationDetailResponse creado exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error en to_response: {str(e)}", exc_info=True)
            raise 