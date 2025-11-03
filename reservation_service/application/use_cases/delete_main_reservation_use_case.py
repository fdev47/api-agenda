"""
Use case para eliminar una main_reservation
"""
import logging
from ...domain.dto.responses.main_reservation_response import MainReservationResponse
from ...domain.interfaces.main_reservation_repository import MainReservationRepository
from ...domain.exceptions.reservation_exceptions import (
    ReservationNotFoundException
)

logger = logging.getLogger(__name__)


class DeleteMainReservationUseCase:
    """Caso de uso para eliminar una main_reservation"""
    
    def __init__(self, main_reservation_repository: MainReservationRepository):
        self.main_reservation_repository = main_reservation_repository
    
    async def execute(self, main_reservation_id: int) -> MainReservationResponse:
        """Ejecutar el caso de uso"""
        logger.info(f"🚀 DeleteMainReservationUseCase.execute() iniciado para main_reservation_id: {main_reservation_id}")
        
        try:
            # Obtener la main_reservation existente
            logger.info("📝 Obteniendo main_reservation existente...")
            main_reservation = await self.main_reservation_repository.get_by_id(main_reservation_id)
            
            if not main_reservation:
                logger.warning(f"⚠️ MainReservation con ID {main_reservation_id} no encontrada")
                raise ReservationNotFoundException(
                    f"MainReservation con ID {main_reservation_id} no encontrada",
                    reservation_id=main_reservation_id
                )
            
            logger.info(f"✅ MainReservation encontrada: ID={main_reservation.id}")
            
            # Convertir a DTO de respuesta antes de eliminar
            logger.info("📝 Convirtiendo a DTO de respuesta...")
            response = self.to_response(main_reservation)
            logger.info("✅ DTO de respuesta creado")
            
            # Eliminar la main_reservation
            logger.info("🗑️ Eliminando main_reservation de la base de datos...")
            success = await self.main_reservation_repository.delete(main_reservation_id)
            
            if not success:
                logger.error(f"❌ Error al eliminar main_reservation {main_reservation_id} de la base de datos")
                raise Exception(f"No se pudo eliminar la main_reservation {main_reservation_id}")
            
            logger.info("✅ MainReservation eliminada exitosamente")
            return response
            
        except ReservationNotFoundException as e:
            logger.warning(f"⚠️ Error de validación en delete_main_reservation: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado en delete_main_reservation: {str(e)}", exc_info=True)
            raise
    
    def to_response(self, main_reservation) -> MainReservationResponse:
        """Convertir entidad a DTO de respuesta"""
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
            order_numbers=main_reservation.sector_data.order_numbers
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

