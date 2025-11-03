"""
Use case para crear una reserva
"""
import logging
from typing import Optional
from datetime import datetime
from typing import List

from ...domain.entities.reservation import Reservation
from ...domain.entities.order_number import OrderNumber
from ...domain.entities.customer_data import CustomerData
from ...domain.entities.branch_data import BranchData
from ...domain.entities.sector_data import SectorData
from ...domain.entities.main_reservation import MainReservation
from ...domain.entities.reservation_status import ReservationStatus
from ...domain.dto.requests.create_reservation_request import CreateReservationRequest
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.interfaces.main_reservation_repository import MainReservationRepository
from ...domain.interfaces.schedule_repository import ScheduleRepository
from ...domain.exceptions.reservation_exceptions import (
    ReservationAlreadyExistsException,
    ReservationValidationException
)

logger = logging.getLogger(__name__)

class CreateReservationUseCase:
    """Caso de uso para crear una nueva reserva"""
    
    def __init__(
        self, 
        reservation_repository: ReservationRepository,
        main_reservation_repository: MainReservationRepository
    ):
        self.reservation_repository = reservation_repository
        self.main_reservation_repository = main_reservation_repository
    
    async def execute(self, request: CreateReservationRequest) -> ReservationResponse:
        """Ejecutar el caso de uso"""
        logger.info(f"🚀 CreateReservationUseCase.execute() iniciado")
        
        try:
            # Convertir DTOs de request a entidades de dominio
            logger.info("🔄 Convirtiendo DTOs a entidades...")
            customer_data = CustomerData(
                customer_id=request.customer_data.customer_id,
                id=request.customer_data.id,
                auth_uid=request.customer_data.auth_uid,
                ruc=request.customer_data.ruc,
                company_name=request.customer_data.company_name,
                email=request.customer_data.email,
                username=request.customer_data.username,
                phone=request.customer_data.phone,
                cellphone_number=request.customer_data.cellphone_number,
                cellphone_country_code=request.customer_data.cellphone_country_code,
                address_id=request.customer_data.address_id,
                is_active=request.customer_data.is_active
            )
            
            # Crear BranchData básico solo con ID (se guardará en BD como null)
            branch_data = BranchData(
                branch_id=request.branch_data.branch_id,
                name=request.branch_data.name,
                code=request.branch_data.code,
                address=request.branch_data.address,
                country_id=request.branch_data.country_id,
                country_name=request.branch_data.country_name,
                state_id=request.branch_data.state_id,
                state_name=request.branch_data.state_name,
                city_id=request.branch_data.city_id,
                city_name=request.branch_data.city_name,
                ramp_id=0,
                ramp_name="N/A"
            )
            
            # Usar el primer sector como referencia para la reserva principal
            first_sector = request.sector_data[0]
            sector_data = SectorData(
                sector_id=first_sector.sector_id,
                name=first_sector.name,
                description=first_sector.description,
                sector_type_id=first_sector.sector_type_id,
                sector_type_name=first_sector.sector_type_name,
                measurement_unit_id=first_sector.measurement_unit_id,
                measurement_unit_name=first_sector.measurement_unit_name,
                capacity=first_sector.capacity,
                pallet_count=0,
                granel_count=0,
                boxes_count=0,
                order_numbers=None
            )
            
            # Crear lista con un order_number dummy
            order_numbers = [OrderNumber(code="N/A", description="")]
            
            # Crear la entidad de reserva principal
            logger.info("🏗️ Creando entidad Reservation...")
            reservation = Reservation(
                user_id=request.user_id,
                customer_id=request.customer_id,
                branch_data=branch_data,
                sector_data=sector_data,
                customer_data=customer_data,
                unloading_time_minutes=request.unloading_time_minutes,
                reason=request.reason,
                order_numbers=order_numbers,
                reservation_date=request.reservation_date,
                start_time=request.start_time,
                end_time=request.end_time,
                notes=request.notes,
                status=ReservationStatus.PENDING,
                cargo_type=request.cargo_type,
                ramp_id=None
            )
            
            # Guardar la reserva principal
            logger.info("💾 Guardando reserva principal en BD...")
            saved_reservation = await self.reservation_repository.create(reservation)
            logger.info(f"✅ Reserva principal guardada con ID: {saved_reservation.id}")
            
            # Crear main_reservations para cada sector
            logger.info(f"📋 Creando {len(request.sector_data)} main_reservations...")
            main_reservations_created = []
            
            for sector_item in request.sector_data:
                logger.info(f"🔄 Procesando sector {sector_item.sector_id} con rampa {sector_item.ramp_id}")
                
                # Convertir sector_data a entidad
                sector_data_entity = SectorData(
                    sector_id=sector_item.sector_id,
                    name=sector_item.name,
                    description=sector_item.description,
                    sector_type_id=sector_item.sector_type_id,
                    sector_type_name=sector_item.sector_type_name,
                    capacity=sector_item.capacity,
                    measurement_unit_id=sector_item.measurement_unit_id,
                    measurement_unit_name=sector_item.measurement_unit_name,
                    pallet_count=getattr(sector_item, 'pallet_count', 0),
                    granel_count=getattr(sector_item, 'granel_count', 0),
                    boxes_count=getattr(sector_item, 'boxes_count', 0),
                    order_numbers=getattr(sector_item, 'order_numbers', None),
                    ramp_id=sector_item.ramp_id,
                    ramp_name=sector_item.ramp_name
                )
                
                # Crear MainReservation
                main_reservation = MainReservation(
                    sector_id=sector_item.sector_id,
                    reservation_id=saved_reservation.id,
                    sector_data=sector_data_entity,
                    reservation_date=request.reservation_date,
                    start_time=request.start_time,
                    end_time=request.end_time
                )
                
                # Guardar main_reservation
                created_main_reservation = await self.main_reservation_repository.create(main_reservation)
                main_reservations_created.append(created_main_reservation)
                logger.info(f"✅ MainReservation creada con ID: {created_main_reservation.id}")
            
            logger.info(f"✅ {len(main_reservations_created)} main_reservations creadas")
            
            # Convertir a DTO de respuesta
            response = self.to_response(saved_reservation, main_reservations_created)
            logger.info("🎉 CreateReservationUseCase completado exitosamente")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error en CreateReservationUseCase: {str(e)}", exc_info=True)
            raise
    
    def to_response(self, reservation: Reservation, main_reservations: List) -> ReservationResponse:
        """Convertir entidad a DTO de respuesta"""
        from ...domain.dto.responses.customer_data_response import CustomerDataResponse
        from ...domain.dto.responses.reservation_response import ReservationResponse
        from ...domain.dto.responses.sector_data_response import SectorDataResponse
        from ...domain.dto.responses.main_reservation_response import MainReservationResponse
        
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
        
        # Convertir main_reservations a responses
        main_reservation_responses = []
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
            
            main_reservation_responses.append(MainReservationResponse(
                id=main_res.id,
                sector_id=main_res.sector_id,
                reservation_id=main_res.reservation_id,
                sector_data=sector_data_response,
                reservation_date=main_res.reservation_date,
                start_time=main_res.start_time,
                end_time=main_res.end_time,
                created_at=main_res.created_at,
                updated_at=main_res.updated_at
            ))
        
        return ReservationResponse(
            id=reservation.id,
            user_id=reservation.user_id,
            customer_id=reservation.customer_id,
            branch_id=reservation.branch_data.branch_id,
            main_reservations=main_reservation_responses,
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