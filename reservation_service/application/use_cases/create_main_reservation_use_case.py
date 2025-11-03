"""
Use case para crear una main_reservation
"""
import logging
from ...domain.dto.requests.create_main_reservation_request import CreateMainReservationRequest
from ...domain.dto.responses.main_reservation_response import MainReservationResponse
from ...domain.interfaces.main_reservation_repository import MainReservationRepository
from ...domain.exceptions.reservation_exceptions import ReservationValidationException

logger = logging.getLogger(__name__)


class CreateMainReservationUseCase:
    """Caso de uso para crear una nueva main_reservation"""
    
    def __init__(self, main_reservation_repository: MainReservationRepository):
        self.main_reservation_repository = main_reservation_repository
    
    async def execute(self, request: CreateMainReservationRequest) -> MainReservationResponse:
        """Ejecutar el caso de uso"""
        logger.info(f"🚀 CreateMainReservationUseCase.execute() iniciado")
        
        try:
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
                order_numbers=getattr(request.sector_data, 'order_numbers', None),
                ramp_id=getattr(request.sector_data, 'ramp_id', None),
                ramp_name=getattr(request.sector_data, 'ramp_name', None)
            )
            
            # Crear la entidad main_reservation
            logger.info("🏗️ Creando entidad MainReservation...")
            main_reservation = MainReservation(
                sector_id=request.sector_id,
                reservation_id=request.reservation_id,
                sector_data=sector_data,
                reservation_date=request.reservation_date,
                start_time=request.start_time,
                end_time=request.end_time
            )
            
            logger.info("✅ Entidad MainReservation creada")
            
            # Guardar en el repositorio
            logger.info("💾 Guardando en el repositorio...")
            created_main_reservation = await self.main_reservation_repository.create(main_reservation)
            logger.info(f"✅ MainReservation creada con ID: {created_main_reservation.id}")
            
            # Convertir a DTO de respuesta
            logger.info("🔄 Convirtiendo a DTO de respuesta...")
            return self.to_response(created_main_reservation)
            
        except ValueError as e:
            logger.error(f"❌ Error de validación: {str(e)}")
            raise ReservationValidationException(str(e))
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
            order_numbers=main_reservation.sector_data.order_numbers,
            ramp_id=main_reservation.sector_data.ramp_id,
            ramp_name=main_reservation.sector_data.ramp_name
        )
        
        return MainReservationResponse(
            id=main_reservation.id,
            sector_id=main_reservation.sector_id,
            reservation_id=main_reservation.reservation_id,
            sector_data=sector_data_response,
            reservation_date=main_reservation.reservation_date,
            start_time=main_reservation.start_time,
            end_time=main_reservation.end_time,
            created_at=main_reservation.created_at,
            updated_at=main_reservation.updated_at
        )

