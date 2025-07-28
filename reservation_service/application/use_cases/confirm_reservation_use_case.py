"""
Use case para confirmar una reserva
"""
import logging
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.exceptions.reservation_exceptions import (
    ReservationNotFoundException,
    ReservationStatusException
)

# Configurar logging
logger = logging.getLogger(__name__)


class ConfirmReservationUseCase:
    """Caso de uso para confirmar una reserva"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(self, reservation_id: int) -> ReservationResponse:
        """Ejecutar el caso de uso"""
        logger.info(f"🚀 ConfirmReservationUseCase.execute() iniciado para reservation_id: {reservation_id}")
        
        try:
            # Obtener la reserva existente
            logger.info("📝 Obteniendo reserva existente...")
            reservation = await self.reservation_repository.get_by_id(reservation_id)
            
            if not reservation:
                logger.warning(f"⚠️ Reserva con ID {reservation_id} no encontrada")
                raise ReservationNotFoundException(
                    f"Reserva con ID {reservation_id} no encontrada",
                    reservation_id=reservation_id
                )
            
            logger.info(f"✅ Reserva encontrada: ID={reservation.id}, status={reservation.status.value}")
            
            # Verificar que la reserva se pueda confirmar
            if reservation.is_cancelled():
                logger.warning(f"⚠️ No se puede confirmar reserva cancelada: ID={reservation.id}, status={reservation.status.value}")
                raise ReservationStatusException(
                    f"No se puede confirmar una reserva cancelada",
                    current_status=reservation.status.value
                )
            
            if reservation.is_completed():
                logger.warning(f"⚠️ No se puede confirmar reserva completada: ID={reservation.id}, status={reservation.status.value}")
                raise ReservationStatusException(
                    f"No se puede confirmar una reserva completada",
                    current_status=reservation.status.value
                )
            
            logger.info("✅ Reserva puede ser confirmada")
            
            # Confirmar la reserva
            logger.info("✅ Confirmando reserva...")
            reservation.confirm()
            logger.info(f"✅ Reserva confirmada: nuevo status={reservation.status.value}")
            
            # Guardar la reserva actualizada
            logger.info("💾 Guardando reserva actualizada en BD...")
            updated_reservation = await self.reservation_repository.update(reservation)
            logger.info("✅ Reserva actualizada guardada exitosamente")
            
            # Convertir a DTO de respuesta
            logger.info("📝 Convirtiendo a DTO de respuesta...")
            response = self.to_response(updated_reservation)
            logger.info("✅ DTO de respuesta creado")
            
            logger.info("🎉 ConfirmReservationUseCase completado exitosamente")
            return response
            
        except (ReservationNotFoundException, ReservationStatusException) as e:
            logger.warning(f"⚠️ Error de validación en confirm_reservation: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado en confirm_reservation: {str(e)}", exc_info=True)
            raise
    
    def to_response(self, reservation) -> ReservationResponse:
        """Convertir entidad a DTO de respuesta"""
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
        
        # Convertir datos del sector
        sector_response = SectorDataResponse(
            sector_id=reservation.sector_data.sector_id,
            name=reservation.sector_data.name,
            description=reservation.sector_data.description,
            sector_type_id=reservation.sector_data.sector_type_id,
            sector_type_name=reservation.sector_data.sector_type_name,
            capacity=reservation.sector_data.capacity,
            measurement_unit_id=reservation.sector_data.measurement_unit_id,
            measurement_unit_name=reservation.sector_data.measurement_unit_name
        )
        
        # Convertir números de pedido
        order_responses = [
            OrderNumberResponse(code=order.code, description=order.description)
            for order in reservation.order_numbers
        ]
        
        return ReservationResponse(
            id=reservation.id,
            user_id=reservation.user_id,
            customer_id=reservation.customer_id,
            branch_data=branch_response,
            sector_data=sector_response,
            customer_data=customer_response,
            unloading_time_minutes=reservation.unloading_time_minutes,
            unloading_time_hours=reservation.get_total_unloading_time_hours(),
            reason=reservation.reason,
            order_numbers=order_responses,
            reservation_date=reservation.reservation_date,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            status=reservation.status.value,
            notes=reservation.notes,
            created_at=reservation.created_at,
            updated_at=reservation.updated_at
        ) 