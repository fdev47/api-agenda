"""
Use case para actualizar una main_reservation
"""
import logging
from ...domain.dto.requests.update_main_reservation_request import UpdateMainReservationRequest
from ...domain.dto.responses.main_reservation_response import MainReservationResponse
from ...domain.interfaces.main_reservation_repository import MainReservationRepository
from ...domain.exceptions.reservation_exceptions import (
    ReservationNotFoundException,
    ReservationValidationException
)

logger = logging.getLogger(__name__)


class UpdateMainReservationUseCase:
    """Caso de uso para actualizar una main_reservation"""
    
    def __init__(self, main_reservation_repository: MainReservationRepository):
        self.main_reservation_repository = main_reservation_repository
    
    async def execute(self, request: UpdateMainReservationRequest) -> MainReservationResponse:
        """Ejecutar el caso de uso"""
        logger.info(f"🚀 UpdateMainReservationUseCase.execute() iniciado para ID: {request.id}")
        
        try:
            # Obtener la main_reservation existente
            logger.info("📝 Obteniendo main_reservation existente...")
            existing_main_reservation = await self.main_reservation_repository.get_by_id(request.id)
            
            if not existing_main_reservation:
                logger.warning(f"⚠️ MainReservation con ID {request.id} no encontrada")
                raise ReservationNotFoundException(
                    f"MainReservation con ID {request.id} no encontrada",
                    reservation_id=request.id
                )
            
            logger.info(f"✅ MainReservation encontrada: ID={existing_main_reservation.id}")
            
            from ...domain.entities.main_reservation import MainReservation
            from ...domain.entities.sector_data import SectorData
            
            logger.info("🔄 Convirtiendo DTOs a entidades...")
            
            # Convertir sector_data a entidad
            sector_data = SectorData(
                sector_id=request.sector_data.sector_id,
                name=request.sector_data.name,
                description=request.sector_data.description,
                sector_type_id=request.sector_data.sector_type_id,
                sector_type_name=request.sector_data.sector_type_name,
                capacity=request.sector_data.capacity,
                measurement_unit_id=request.sector_data.measurement_unit_id,
                measurement_unit_name=request.sector_data.measurement_unit_name,
                pallet_count=getattr(request.sector_data, 'pallet_count', 0),
                granel_count=getattr(request.sector_data, 'granel_count', 0),
                boxes_count=getattr(request.sector_data, 'boxes_count', 0),
                order_numbers=getattr(request.sector_data, 'order_numbers', None)
            )
            
            # Crear la entidad main_reservation actualizada
            logger.info("🏗️ Creando entidad MainReservation actualizada...")
            updated_main_reservation = MainReservation(
                id=request.id,
                sector_id=request.sector_id,
                reservation_id=request.reservation_id,
                ramp_id=request.ramp_id,
                sector_data=sector_data,
                reservation_date=request.reservation_date,
                start_time=request.start_time,
                end_time=request.end_time,
                created_at=existing_main_reservation.created_at,  # Preservar created_at original
                updated_at=None  # Se actualizará automáticamente
            )
            
            logger.info("✅ Entidad MainReservation actualizada creada")
            
            # Actualizar en el repositorio
            logger.info("💾 Actualizando en el repositorio...")
            saved_main_reservation = await self.main_reservation_repository.update(updated_main_reservation)
            logger.info(f"✅ MainReservation actualizada con ID: {saved_main_reservation.id}")
            
            # Convertir a DTO de respuesta
            logger.info("🔄 Convirtiendo a DTO de respuesta...")
            return self.to_response(saved_main_reservation)
            
        except (ReservationNotFoundException, ValueError) as e:
            logger.error(f"❌ Error de validación: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
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

