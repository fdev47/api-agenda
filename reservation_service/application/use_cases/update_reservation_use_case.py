"""
Use case para actualizar una reserva
"""
import logging
from datetime import datetime
from typing import List, Optional

from ...domain.entities.order_number import OrderNumber
from ...domain.dto.requests.update_reservation_request import UpdateReservationRequest
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.entities.reservation import Reservation
from ...domain.exceptions.reservation_exceptions import (
    ReservationNotFoundException,
    ReservationAlreadyExistsException,
    ReservationStatusException
)

logger = logging.getLogger(__name__)

class UpdateReservationUseCase:
    """Caso de uso para actualizar una reserva"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(self, reservation_id: int, request: UpdateReservationRequest) -> ReservationResponse:
        """Ejecutar el caso de uso"""
        logger.info(f"🚀 UpdateReservationUseCase.execute() iniciado para ID: {reservation_id}")
        
        try:
            # Obtener la reserva existente
            logger.info(f"🔍 Buscando reserva con ID: {reservation_id}")
            reservation = await self.reservation_repository.get_by_id(reservation_id)
            
            if not reservation:
                logger.warning(f"⚠️ Reserva no encontrada: {reservation_id}")
                raise ReservationNotFoundException(
                    f"Reserva con ID {reservation_id} no encontrada",
                    reservation_id=reservation_id
                )
            
            logger.info(f"✅ Reserva encontrada: {reservation.id}")
            
            # Verificar que la reserva se pueda actualizar
            if reservation.is_cancelled():
                logger.warning(f"⚠️ No se puede actualizar reserva cancelada: {reservation.status.value}")
                raise ReservationStatusException(
                    f"No se puede actualizar una reserva cancelada",
                    current_status=reservation.status.value
                )
            
            if reservation.is_completed():
                logger.warning(f"⚠️ No se puede actualizar reserva completada: {reservation.status.value}")
                raise ReservationStatusException(
                    f"No se puede actualizar una reserva completada",
                    current_status=reservation.status.value
                )
            
            logger.info("✅ Validaciones de estado pasadas")
            
            # Actualizar campos si están presentes en el request
            if request.unloading_time_minutes is not None:
                logger.info(f"📝 Actualizando unloading_time_minutes: {request.unloading_time_minutes}")
                reservation.unloading_time_minutes = request.unloading_time_minutes
            
            if request.reason is not None:
                logger.info(f"📝 Actualizando reason: {request.reason}")
                reservation.reason = request.reason
            
            if request.cargo_type is not None:
                logger.info(f"📝 Actualizando cargo_type: {request.cargo_type}")
                reservation.cargo_type = request.cargo_type
            
            if request.notes is not None:
                logger.info(f"📝 Actualizando notes: {request.notes}")
                reservation.notes = request.notes
            
            if request.order_numbers is not None:
                logger.info(f"📝 Actualizando order_numbers: {len(request.order_numbers)} pedidos")
                # Convertir números de pedido
                order_numbers = [
                    OrderNumber(code=order.code, description=order.description)
                    for order in request.order_numbers
                ]
                reservation.order_numbers = order_numbers
            
            # Actualizar horarios si están presentes
            if request.start_time is not None:
                logger.info(f"📝 Actualizando start_time: {request.start_time}")
                reservation.start_time = request.start_time
            
            if request.end_time is not None:
                logger.info(f"📝 Actualizando end_time: {request.end_time}")
                reservation.end_time = request.end_time
            
            # Actualizar datos del sector si están presentes
            if request.sector_data is not None:
                logger.info("📝 Actualizando sector_data...")
                if request.sector_data.name is not None:
                    reservation.sector_data.name = request.sector_data.name
                if request.sector_data.description is not None:
                    reservation.sector_data.description = request.sector_data.description
                if request.sector_data.sector_type_id is not None:
                    reservation.sector_data.sector_type_id = request.sector_data.sector_type_id
                if request.sector_data.sector_type_name is not None:
                    reservation.sector_data.sector_type_name = request.sector_data.sector_type_name
                if request.sector_data.measurement_unit_id is not None:
                    reservation.sector_data.measurement_unit_id = request.sector_data.measurement_unit_id
                if request.sector_data.measurement_unit_name is not None:
                    reservation.sector_data.measurement_unit_name = request.sector_data.measurement_unit_name
                if request.sector_data.capacity is not None:
                    reservation.sector_data.capacity = request.sector_data.capacity
                logger.info("✅ sector_data actualizado")
            
            # Actualizar datos de la sucursal si están presentes
            if request.branch_data is not None:
                logger.info("📝 Actualizando branch_data...")
                if request.branch_data.name is not None:
                    reservation.branch_data.name = request.branch_data.name
                if request.branch_data.code is not None:
                    reservation.branch_data.code = request.branch_data.code
                if request.branch_data.address is not None:
                    reservation.branch_data.address = request.branch_data.address
                if request.branch_data.country_id is not None:
                    reservation.branch_data.country_id = request.branch_data.country_id
                if request.branch_data.country_name is not None:
                    reservation.branch_data.country_name = request.branch_data.country_name
                if request.branch_data.state_id is not None:
                    reservation.branch_data.state_id = request.branch_data.state_id
                if request.branch_data.state_name is not None:
                    reservation.branch_data.state_name = request.branch_data.state_name
                if request.branch_data.city_id is not None:
                    reservation.branch_data.city_id = request.branch_data.city_id
                if request.branch_data.city_name is not None:
                    reservation.branch_data.city_name = request.branch_data.city_name
                logger.info("✅ branch_data actualizado")
            
            # Actualizar datos del cliente si están presentes
            if request.customer_data is not None:
                logger.info("📝 Actualizando customer_data...")
                if request.customer_data.customer_id is not None:
                    reservation.customer_data.customer_id = request.customer_data.customer_id
                if request.customer_data.id is not None:
                    reservation.customer_data.id = request.customer_data.id
                if request.customer_data.auth_uid is not None:
                    reservation.customer_data.auth_uid = request.customer_data.auth_uid
                if request.customer_data.ruc is not None:
                    reservation.customer_data.ruc = request.customer_data.ruc
                if request.customer_data.company_name is not None:
                    reservation.customer_data.company_name = request.customer_data.company_name
                if request.customer_data.email is not None:
                    reservation.customer_data.email = request.customer_data.email
                if request.customer_data.username is not None:
                    reservation.customer_data.username = request.customer_data.username
                if request.customer_data.phone is not None:
                    reservation.customer_data.phone = request.customer_data.phone
                if request.customer_data.cellphone_number is not None:
                    reservation.customer_data.cellphone_number = request.customer_data.cellphone_number
                if request.customer_data.cellphone_country_code is not None:
                    reservation.customer_data.cellphone_country_code = request.customer_data.cellphone_country_code
                if request.customer_data.address_id is not None:
                    reservation.customer_data.address_id = request.customer_data.address_id
                if request.customer_data.is_active is not None:
                    reservation.customer_data.is_active = request.customer_data.is_active
                logger.info("✅ customer_data actualizado")
            
            # Verificar conflictos de horario si se actualizaron los horarios
            if request.start_time is not None or request.end_time is not None:
                logger.info("🔍 Verificando conflictos de horario...")
                conflicts = await self.reservation_repository.check_conflicts(
                    branch_id=reservation.get_branch_id(),
                    sector_id=reservation.get_sector_id(),
                    start_time=reservation.start_time,
                    end_time=reservation.end_time,
                    exclude_reservation_id=reservation_id
                )
                
                if conflicts:
                    logger.warning(f"⚠️ Conflicto de horario detectado: {len(conflicts)} reservas conflictivas")
                    raise ReservationAlreadyExistsException(
                        f"Ya existe una reserva en el horario {reservation.start_time.strftime('%H:%M')}-{reservation.end_time.strftime('%H:%M')} "
                        f"para la sucursal {reservation.get_branch_id()} y sector {reservation.get_sector_id()}",
                        branch_id=reservation.get_branch_id(),
                        sector_id=reservation.get_sector_id(),
                        start_time=reservation.start_time,
                        end_time=reservation.end_time
                    )
                
                logger.info("✅ No se detectaron conflictos de horario")
            
            # Actualizar timestamp
            reservation.updated_at = datetime.utcnow()
            logger.info("📝 Timestamp actualizado")
            
            # Guardar la reserva actualizada
            logger.info("💾 Guardando reserva actualizada...")
            updated_reservation = await self.reservation_repository.update(reservation)
            logger.info(f"✅ Reserva actualizada exitosamente con ID: {updated_reservation.id}")
            
            # Convertir a DTO de respuesta
            response = self.to_response(updated_reservation)
            logger.info("🎉 UpdateReservationUseCase completado exitosamente")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error en UpdateReservationUseCase: {str(e)}", exc_info=True)
            raise
    
    def to_response(self, reservation: Reservation) -> ReservationResponse:
        """Convertir entidad a DTO de respuesta"""
        try:
            logger.info("🔄 Convirtiendo entidad a DTO de respuesta...")
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
            logger.info("✅ CustomerDataResponse creado")
            
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
            logger.info("✅ BranchDataResponse creado")
            
            # Convertir datos del sector
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
            order_responses = [
                OrderNumberResponse(code=order.code, description=order.description)
                for order in reservation.order_numbers
            ]
            logger.info(f"✅ OrderNumberResponse creados: {len(order_responses)} pedidos")
            
            response = ReservationResponse(
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
                order_numbers=order_responses,
                reservation_date=reservation.reservation_date,
                start_time=reservation.start_time,
                end_time=reservation.end_time,
                status=reservation.status.value,
                notes=reservation.notes,
                created_at=reservation.created_at,
                updated_at=reservation.updated_at
            )
            logger.info("✅ ReservationResponse creado exitosamente")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error en to_response: {str(e)}", exc_info=True)
            raise 