"""
Use case para obtener una main_reservation
"""
import logging
from ...domain.dto.responses.main_reservation_response import MainReservationResponse
from ...domain.interfaces.main_reservation_repository import MainReservationRepository
from ...domain.exceptions.reservation_exceptions import ReservationNotFoundException

logger = logging.getLogger(__name__)


class GetMainReservationUseCase:
    """Caso de uso para obtener una main_reservation por ID"""
    
    def __init__(self, main_reservation_repository: MainReservationRepository):
        self.main_reservation_repository = main_reservation_repository
    
    async def execute(self, main_reservation_id: int) -> MainReservationResponse:
        """Ejecutar el caso de uso"""
        try:
            logger.info(f"🔍 Buscando main_reservation con ID: {main_reservation_id}")
            
            # Buscar la main_reservation
            main_reservation = await self.main_reservation_repository.get_by_id(main_reservation_id)
            
            if not main_reservation:
                logger.warning(f"⚠️ MainReservation no encontrada: {main_reservation_id}")
                raise ReservationNotFoundException(
                    f"MainReservation con ID {main_reservation_id} no encontrada",
                    reservation_id=main_reservation_id
                )
            
            logger.info(f"✅ MainReservation encontrada: {main_reservation.id}")
            logger.info("🔄 Convirtiendo a DTO de respuesta...")
            
            # Convertir a DTO de respuesta
            result = self.to_response(main_reservation)
            logger.info("✅ Conversión completada exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error en GetMainReservationUseCase.execute(): {str(e)}", exc_info=True)
            raise
    
    def to_response(self, main_reservation) -> MainReservationResponse:
        """Convertir entidad a DTO de respuesta"""
        try:
            from ...domain.dto.responses.sector_data_response import SectorDataResponse
            
            # Convertir sector_data
            sector_data_response = SectorDataResponse(
                sector_id=main_reservation.sector_data.sector_id,
                name=main_reservation.sector_data.name,
                description=main_reservation.sector_data.description,
                sector_type_id=main_reservation.sector_data.sector_type_id,
                sector_type_name=main_reservation.sector_data.sector_type_name,
                capacity=main_reservation.sector_data.capacity,
                measurement_unit_id=main_reservation.sector_data.measurement_unit_id,
                measurement_unit_name=main_reservation.sector_data.measurement_unit_name,
                pallet_count=main_reservation.sector_data.pallet_count,
                granel_count=main_reservation.sector_data.granel_count,
                boxes_count=main_reservation.sector_data.boxes_count,
                order_numbers=main_reservation.sector_data.order_numbers,
                ramp_id=main_reservation.sector_data.ramp_id,
                ramp_name=main_reservation.sector_data.ramp_name
            )
            
            return MainReservationResponse(
                id=main_reservation.id,
                sector_id=main_reservation.sector_id,
                reservation_id=main_reservation.reservation_id,
                ramp_id=main_reservation.ramp_id,
                sector_data=sector_data_response,
                reservation_date=main_reservation.reservation_date,
                start_time=main_reservation.start_time,
                end_time=main_reservation.end_time,
                created_at=main_reservation.created_at,
                updated_at=main_reservation.updated_at
            )
        except Exception as e:
            logger.error(f"❌ Error en to_response: {str(e)}", exc_info=True)
            raise

