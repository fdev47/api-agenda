"""
Use case para obtener una reserva
"""
import logging
from ...domain.dto.responses.reservation_detail_response import ReservationDetailResponse
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.exceptions.reservation_exceptions import ReservationNotFoundException

logger = logging.getLogger(__name__)


class GetReservationUseCase:
    """Caso de uso para obtener una reserva por ID"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository
    
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
            logger.info("🔄 Convirtiendo a DTO de respuesta...")
            
            # Convertir a DTO de respuesta
            result = self.to_response(reservation)
            logger.info("✅ Conversión completada exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error en GetReservationUseCase.execute(): {str(e)}", exc_info=True)
            raise
    
    def to_response(self, reservation) -> ReservationDetailResponse:
        """Convertir entidad a DTO de respuesta"""
        try:
            logger.info("🔄 Iniciando conversión a DTO...")
            
            from ...domain.dto.responses.customer_data_response import CustomerDataResponse
            from ...domain.dto.responses.branch_data_response import BranchDataResponse
            from ...domain.dto.responses.sector_data_response import SectorDataResponse
            from ...domain.dto.responses.order_number_response import OrderNumberResponse
            
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
                city_name=reservation.branch_data.city_name,
                ramp_id=reservation.branch_data.ramp_id,
                ramp_name=reservation.branch_data.ramp_name
            )
            logger.info("✅ BranchDataResponse creado")
            
            # Convertir datos del sector
            logger.info("🔄 Convirtiendo datos del sector...")
            sector_response = SectorDataResponse(
                sector_id=reservation.sector_data.sector_id,
                name=reservation.sector_data.name,
                description=reservation.sector_data.description,
                sector_type_id=reservation.sector_data.sector_type_id,
                sector_type_name=reservation.sector_data.sector_type_name,
                measurement_unit_id=reservation.sector_data.measurement_unit_id,
                measurement_unit_name=reservation.sector_data.measurement_unit_name,
                capacity=reservation.sector_data.capacity
            )
            logger.info("✅ SectorDataResponse creado")
            
            # Convertir números de pedido
            logger.info("🔄 Convirtiendo números de pedido...")
            order_responses = [
                OrderNumberResponse(code=order.code, description=order.description)
                for order in reservation.order_numbers
            ]
            logger.info(f"✅ {len(order_responses)} números de pedido convertidos")
            
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
                sector_data=sector_response,
                customer_data=customer_response,
                unloading_time_minutes=reservation.unloading_time_minutes,
                unloading_time_hours=reservation.get_total_unloading_time_hours(),
                reason=reservation.reason,
                cargo_type=reservation.cargo_type,
                ramp_id=reservation.ramp_id,
                order_numbers=order_responses,
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