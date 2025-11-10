"""
Implementación del repositorio de reservas
"""
from typing import List, Optional, Tuple
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
import logging

from ...domain.entities.reservation import Reservation
from ...domain.entities.reservation_status import ReservationStatus
from ...domain.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.exceptions.reservation_exceptions import ReservationNotFoundException
from ...infrastructure.models.reservation import ReservationModel, ReservationOrderNumberModel
from commons.database import get_db_session

# Configurar logging
logger = logging.getLogger(__name__)

class ReservationRepositoryImpl(ReservationRepository):
    """Implementación del repositorio para reservas"""
    
    def __init__(self):
        pass
    
    async def create(self, reservation: Reservation) -> Reservation:
        """Crear una nueva reserva"""
        logger.info("💾 ReservationRepositoryImpl.create() iniciado")
        
        async for session in get_db_session():
            logger.info(f"🔍 Session obtenida: {session}")
            if session is None:
                logger.error("❌ Session es None!")
                raise Exception("No se pudo obtener una sesión de base de datos")
            
            try:
                # Convertir entidad de dominio a modelo de BD
                reservation_model = ReservationModel.from_domain(reservation)
                logger.info("✅ ReservationModel creado correctamente")
                
                # Agregar números de pedido
                for order in reservation.order_numbers:
                    order_model = ReservationOrderNumberModel(
                        code=order.code,
                        description=order.description
                    )
                    reservation_model.order_numbers.append(order_model)
                
                session.add(reservation_model)
                logger.info("✅ ReservationModel agregado a la sesión")
                await session.commit()
                logger.info("✅ Commit realizado")
                await session.refresh(reservation_model)
                logger.info("✅ Refresh realizado")
                
                # Cargar explícitamente las relaciones antes de convertir a dominio
                await session.refresh(reservation_model, attribute_names=['order_numbers'])
                logger.info("✅ Relaciones cargadas explícitamente")
                
                logger.info(f"✅ Reserva creada en BD con ID: {reservation_model.id}")
                return reservation_model.to_domain()
                
            except Exception as e:
                logger.error(f"❌ Error en ReservationRepositoryImpl.create(): {str(e)}", exc_info=True)
                await session.rollback()
                raise
    
    async def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """Obtener una reserva por ID"""
        async for session in get_db_session():
            result = await session.execute(
                select(ReservationModel).where(ReservationModel.id == reservation_id)
            )
            reservation_model = result.scalar_one_or_none()
            
            if not reservation_model:
                return None
            
            # Cargar explícitamente las relaciones
            await session.refresh(reservation_model, attribute_names=['order_numbers'])
            
            return reservation_model.to_domain()
    
    async def list(self, filter_request: ReservationFilterRequest) -> Tuple[List[Reservation], int]:
        """Listar reservas con filtros y paginación"""
        async for session in get_db_session():
            # Construir la consulta base
            query = select(ReservationModel)
            
            # Aplicar filtros
            conditions = []
            
            if filter_request.user_id:
                conditions.append(ReservationModel.user_id == filter_request.user_id)
            
            if filter_request.customer_id:
                conditions.append(ReservationModel.customer_id == filter_request.customer_id)
            
            if filter_request.branch_id:
                conditions.append(ReservationModel.branch_id == filter_request.branch_id)
            
            if filter_request.sector_id:
                conditions.append(ReservationModel.sector_id == filter_request.sector_id)
            
            if filter_request.branch_name:
                conditions.append(ReservationModel.branch_data['name'].astext.ilike(f"%{filter_request.branch_name}%"))
            
            if filter_request.branch_code:
                # Usar filtro exacto para branch_code con sintaxis correcta de PostgreSQL JSON
                conditions.append(func.json_extract_path_text(ReservationModel.branch_data, 'code') == filter_request.branch_code)
            
            if filter_request.sector_name:
                conditions.append(ReservationModel.sector_data['name'].astext.ilike(f"%{filter_request.sector_name}%"))
            
            if filter_request.customer_name:
                conditions.append(ReservationModel.customer_data['company_name'].astext.ilike(f"%{filter_request.customer_name}%"))
            
            if filter_request.customer_email:
                conditions.append(ReservationModel.customer_data['email'].astext.ilike(f"%{filter_request.customer_email}%"))
            
            if filter_request.reservation_date_from:
                conditions.append(ReservationModel.reservation_date >= filter_request.reservation_date_from)
            
            if filter_request.reservation_date_to:
                conditions.append(ReservationModel.reservation_date <= filter_request.reservation_date_to)
            
            if filter_request.status:
                # Manejar múltiples estados separados por comas
                if "," in filter_request.status:
                    status_list = [status.strip() for status in filter_request.status.split(",")]
                    status_conditions = []
                    for status_str in status_list:
                        try:
                            status_enum = ReservationStatus(status_str)
                            status_conditions.append(ReservationModel.status == status_enum)
                        except ValueError:
                            logger.warning(f"⚠️ Estado inválido ignorado: {status_str}")
                    
                    if status_conditions:
                        conditions.append(or_(*status_conditions))
                else:
                    # Estado único
                    try:
                        status_enum = ReservationStatus(filter_request.status)
                        conditions.append(ReservationModel.status == status_enum)
                    except ValueError:
                        logger.warning(f"⚠️ Estado inválido ignorado: {filter_request.status}")
            
            if filter_request.order_code:
                # Para el filtro de order_code necesitamos hacer un join
                query = query.join(ReservationOrderNumberModel)
                conditions.append(ReservationOrderNumberModel.code.ilike(f"%{filter_request.order_code}%"))
            
            if filter_request.cargo_type:
                conditions.append(ReservationModel.cargo_type.ilike(f"%{filter_request.cargo_type}%"))
            
            # Aplicar condiciones si existen
            if conditions:
                query = query.where(and_(*conditions))
            
            # Contar total
            count_query = select(func.count()).select_from(query.subquery())
            result = await session.execute(count_query)
            total = result.scalar()
            
            # Aplicar paginación y ordenamiento
            query = query.offset(filter_request.offset).limit(filter_request.limit)
            query = query.order_by(ReservationModel.reservation_date.desc(), ReservationModel.start_time.desc())
            
            # Ejecutar consulta
            result = await session.execute(query)
            reservation_models = result.scalars().all()
            
            # Cargar explícitamente las relaciones para cada modelo
            for model in reservation_models:
                await session.refresh(model, attribute_names=['order_numbers'])
            
            reservations = [model.to_domain() for model in reservation_models]
            
            return reservations, total
    
    async def update(self, reservation: Reservation) -> Reservation:
        """Actualizar una reserva"""
        async for session in get_db_session():
            query = select(ReservationModel).where(ReservationModel.id == reservation.id)
            result = await session.execute(query)
            reservation_model = result.scalar_one_or_none()
            
            if not reservation_model:
                raise ReservationNotFoundException(
                    f"No se encontró la reserva con ID {reservation.id}",
                    reservation_id=reservation.id
                )
            
            # Actualizar campos básicos
            reservation_model.user_id = reservation.user_id
            reservation_model.customer_id = reservation.customer_id
            reservation_model.branch_id = reservation.branch_data.branch_id
            reservation_model.sector_id = reservation.sector_data.sector_id
            reservation_model.unloading_time_minutes = reservation.unloading_time_minutes
            reservation_model.reason = reservation.reason
            reservation_model.cargo_type = reservation.cargo_type
            reservation_model.reservation_date = reservation.reservation_date
            reservation_model.start_time = reservation.start_time
            reservation_model.end_time = reservation.end_time
            reservation_model.status = reservation.status
            reservation_model.notes = reservation.notes
            reservation_model.closing_summary = reservation.closing_summary
            
            # Actualizar datos JSON
            reservation_model.branch_data = {
                "branch_id": reservation.branch_data.branch_id,
                "name": reservation.branch_data.name,
                "code": reservation.branch_data.code,
                "address": reservation.branch_data.address,
                "country_id": reservation.branch_data.country_id,
                "country_name": reservation.branch_data.country_name,
                "state_id": reservation.branch_data.state_id,
                "state_name": reservation.branch_data.state_name,
                "city_id": reservation.branch_data.city_id,
                "city_name": reservation.branch_data.city_name,
                "ramp_id": reservation.branch_data.ramp_id,
                "ramp_name": reservation.branch_data.ramp_name
            }
            
            reservation_model.sector_data = {
                "sector_id": reservation.sector_data.sector_id,
                "name": reservation.sector_data.name,
                "description": reservation.sector_data.description,
                "sector_type_id": reservation.sector_data.sector_type_id,
                "sector_type_name": reservation.sector_data.sector_type_name,
                "measurement_unit_id": reservation.sector_data.measurement_unit_id,
                "measurement_unit_name": reservation.sector_data.measurement_unit_name,
                "capacity": reservation.sector_data.capacity
            }
            
            reservation_model.customer_data = {
                "customer_id": reservation.customer_data.customer_id,
                "id": str(reservation.customer_data.id) if reservation.customer_data.id else None,
                "auth_uid": reservation.customer_data.auth_uid,
                "ruc": reservation.customer_data.ruc,
                "company_name": reservation.customer_data.company_name,
                "email": reservation.customer_data.email,
                "username": reservation.customer_data.username,
                "phone": reservation.customer_data.phone,
                "cellphone_number": reservation.customer_data.cellphone_number,
                "cellphone_country_code": reservation.customer_data.cellphone_country_code,
                "address_id": str(reservation.customer_data.address_id) if reservation.customer_data.address_id else None,
                "is_active": reservation.customer_data.is_active
            }
            
            # Actualizar números de pedido (eliminar existentes y agregar nuevos)
            delete_query = select(ReservationOrderNumberModel).where(
                ReservationOrderNumberModel.reservation_id == reservation.id
            )
            result = await session.execute(delete_query)
            order_numbers_to_delete = result.scalars().all()
            for order_number in order_numbers_to_delete:
                await session.delete(order_number)
            
            for order in reservation.order_numbers:
                order_model = ReservationOrderNumberModel(
                    reservation_id=reservation.id,
                    code=order.code,
                    description=order.description
                )
                session.add(order_model)
            
            await session.commit()
            await session.refresh(reservation_model)
            
            # Cargar explícitamente las relaciones
            await session.refresh(reservation_model, attribute_names=['order_numbers'])
            
            return reservation_model.to_domain()
    
    async def delete(self, reservation_id: int) -> bool:
        """Eliminar una reserva y todos sus datos relacionados"""
        logger.info(f"🗑️ Eliminando reserva con ID: {reservation_id}")
        
        async for session in get_db_session():
            try:
                # Obtener la reserva
                query = select(ReservationModel).where(ReservationModel.id == reservation_id)
                result = await session.execute(query)
                reservation_model = result.scalar_one_or_none()
                
                if not reservation_model:
                    logger.warning(f"⚠️ Reserva con ID {reservation_id} no encontrada")
                    return False
                
                logger.info(f"✅ Reserva encontrada: ID={reservation_model.id}, status={reservation_model.status}")
                
                # Eliminar números de pedido relacionados primero
                logger.info("🗑️ Eliminando números de pedido relacionados...")
                order_numbers_query = select(ReservationOrderNumberModel).where(
                    ReservationOrderNumberModel.reservation_id == reservation_id
                )
                order_numbers_result = await session.execute(order_numbers_query)
                order_numbers_to_delete = order_numbers_result.scalars().all()
                
                logger.info(f"📊 Encontrados {len(order_numbers_to_delete)} números de pedido para eliminar")
                
                for order_number in order_numbers_to_delete:
                    await session.delete(order_number)
                    logger.debug(f"🗑️ Eliminado número de pedido: {order_number.code}")
                
                # Eliminar la reserva
                logger.info("🗑️ Eliminando la reserva...")
                await session.delete(reservation_model)
                
                # Commit de todos los cambios
                await session.commit()
                logger.info("✅ Reserva y datos relacionados eliminados exitosamente")
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Error al eliminar reserva {reservation_id}: {str(e)}", exc_info=True)
                await session.rollback()
                raise
    
    async def exists_conflict(self, branch_id: int, sector_id: int, start_time: datetime, end_time: datetime, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un conflicto de horario"""
        async for session in get_db_session():
            query = select(ReservationModel).where(
                and_(
                    ReservationModel.branch_id == branch_id,
                    ReservationModel.sector_id == sector_id,
                    ReservationModel.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED]),
                    or_(
                        # Caso 1: La nueva reserva empieza durante una reserva existente
                        and_(start_time >= ReservationModel.start_time, start_time < ReservationModel.end_time),
                        # Caso 2: La nueva reserva termina durante una reserva existente
                        and_(end_time > ReservationModel.start_time, end_time <= ReservationModel.end_time),
                        # Caso 3: La nueva reserva contiene completamente una reserva existente
                        and_(start_time <= ReservationModel.start_time, end_time >= ReservationModel.end_time)
                    )
                )
            )
            
            if exclude_id:
                query = query.where(ReservationModel.id != exclude_id)
            
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None
    
    async def check_conflicts(self, branch_id: int, sector_id: int, start_time: datetime, end_time: datetime, exclude_reservation_id: Optional[int] = None) -> List[Reservation]:
        """Verificar conflictos de horario y retornar las reservas que causan conflicto"""
        async for session in get_db_session():
            query = select(ReservationModel).where(
                and_(
                    ReservationModel.branch_id == branch_id,
                    ReservationModel.sector_id == sector_id,
                    ReservationModel.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED]),
                    or_(
                        # Caso 1: La nueva reserva empieza durante una reserva existente
                        and_(start_time >= ReservationModel.start_time, start_time < ReservationModel.end_time),
                        # Caso 2: La nueva reserva termina durante una reserva existente
                        and_(end_time > ReservationModel.start_time, end_time <= ReservationModel.end_time),
                        # Caso 3: La nueva reserva contiene completamente una reserva existente
                        and_(start_time <= ReservationModel.start_time, end_time >= ReservationModel.end_time)
                    )
                )
            )
            
            if exclude_reservation_id:
                query = query.where(ReservationModel.id != exclude_reservation_id)
            
            result = await session.execute(query)
            reservation_models = result.scalars().all()
            
            # Cargar explícitamente las relaciones para cada modelo
            for model in reservation_models:
                await session.refresh(model, attribute_names=['order_numbers'])
            
            return [model.to_domain() for model in reservation_models]
    
    async def get_conflicting_reservation(self, branch_id: int, sector_id: int, start_time: datetime, end_time: datetime, exclude_id: Optional[int] = None) -> Optional[Reservation]:
        """Obtener la reserva que causa conflicto de horario"""
        async for session in get_db_session():
            query = select(ReservationModel).where(
                and_(
                    ReservationModel.branch_id == branch_id,
                    ReservationModel.sector_id == sector_id,
                    ReservationModel.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED]),
                    or_(
                        and_(start_time >= ReservationModel.start_time, start_time < ReservationModel.end_time),
                        and_(end_time > ReservationModel.start_time, end_time <= ReservationModel.end_time),
                        and_(start_time <= ReservationModel.start_time, end_time >= ReservationModel.end_time)
                    )
                )
            )
            
            if exclude_id:
                query = query.where(ReservationModel.id != exclude_id)
            
            result = await session.execute(query)
            reservation_model = result.scalar_one_or_none()
            
            if not reservation_model:
                return None
            
            # Cargar explícitamente las relaciones
            await session.refresh(reservation_model, attribute_names=['order_numbers'])
            
            return reservation_model.to_domain()
    
    async def get_by_user_id(self, user_id: int, limit: int = 10) -> List[Reservation]:
        """Obtener reservas por usuario"""
        async for session in get_db_session():
            query = select(ReservationModel).where(
                ReservationModel.user_id == user_id
            ).order_by(ReservationModel.reservation_date.desc(), ReservationModel.start_time.desc()).limit(limit)
            
            result = await session.execute(query)
            reservation_models = result.scalars().all()
            
            # Cargar explícitamente las relaciones para cada modelo
            for model in reservation_models:
                await session.refresh(model, attribute_names=['order_numbers'])
            
            return [model.to_domain() for model in reservation_models]
    
    async def get_by_customer_id(self, customer_id: int, limit: int = 10) -> List[Reservation]:
        """Obtener reservas por cliente"""
        async for session in get_db_session():
            query = select(ReservationModel).where(
                ReservationModel.customer_id == customer_id
            ).order_by(ReservationModel.reservation_date.desc(), ReservationModel.start_time.desc()).limit(limit)
            
            result = await session.execute(query)
            reservation_models = result.scalars().all()
            
            # Cargar explícitamente las relaciones para cada modelo
            for model in reservation_models:
                await session.refresh(model, attribute_names=['order_numbers'])
            
            return [model.to_domain() for model in reservation_models]
    
    async def get_by_branch_id(self, branch_id: int, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> List[Reservation]:
        """Obtener reservas por sucursal"""
        async for session in get_db_session():
            query = select(ReservationModel).where(
                ReservationModel.branch_id == branch_id
            )
            
            if date_from:
                query = query.where(ReservationModel.reservation_date >= date_from)
            
            if date_to:
                query = query.where(ReservationModel.reservation_date <= date_to)
            
            query = query.order_by(ReservationModel.reservation_date, ReservationModel.start_time)
            
            result = await session.execute(query)
            reservation_models = result.scalars().all()
            
            # Cargar explícitamente las relaciones para cada modelo
            for model in reservation_models:
                await session.refresh(model, attribute_names=['order_numbers'])
            
            return [model.to_domain() for model in reservation_models]
    
    async def get_by_sector_id(self, sector_id: int, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> List[Reservation]:
        """Obtener reservas por sector"""
        async for session in get_db_session():
            query = select(ReservationModel).where(
                ReservationModel.sector_id == sector_id
            )
            
            if date_from:
                query = query.where(ReservationModel.reservation_date >= date_from)
            
            if date_to:
                query = query.where(ReservationModel.reservation_date <= date_to)
            
            query = query.order_by(ReservationModel.reservation_date, ReservationModel.start_time)
            
            result = await session.execute(query)
            reservation_models = result.scalars().all()
            
            # Cargar explícitamente las relaciones para cada modelo
            for model in reservation_models:
                await session.refresh(model, attribute_names=['order_numbers'])
            
            return [model.to_domain() for model in reservation_models]
    
    async def get_active_reservations(self, branch_id: Optional[int] = None, sector_id: Optional[int] = None) -> List[Reservation]:
        """Obtener reservas activas (pendientes o confirmadas)"""
        async for session in get_db_session():
            query = select(ReservationModel).where(
                ReservationModel.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED])
            )
            
            if branch_id:
                query = query.where(ReservationModel.branch_id == branch_id)
            
            if sector_id:
                query = query.where(ReservationModel.sector_id == sector_id)
            
            query = query.order_by(ReservationModel.reservation_date, ReservationModel.start_time)
            
            result = await session.execute(query)
            reservation_models = result.scalars().all()
            
            # Cargar explícitamente las relaciones para cada modelo
            for model in reservation_models:
                await session.refresh(model, attribute_names=['order_numbers'])
            
            return [model.to_domain() for model in reservation_models]
    
    async def update_status(self, reservation_id: int, status: str) -> bool:
        """Actualizar solo el estado de una reserva"""
        async for session in get_db_session():
            query = select(ReservationModel).where(ReservationModel.id == reservation_id)
            result = await session.execute(query)
            reservation_model = result.scalar_one_or_none()
            
            if not reservation_model:
                return False
            
            reservation_model.status = ReservationStatus(status)
            reservation_model.updated_at = datetime.utcnow()
            
            await session.commit()
            
            return True
    
    async def get_by_period(self, branch_id: int, start_time: datetime, end_time: datetime, status: Optional[str] = None) -> List[Reservation]:
        """Obtener reservas por período de tiempo en una sucursal"""
        logger.info(f"📅 Obteniendo reservas para sucursal {branch_id} entre {start_time} y {end_time}")
        
        async for session in get_db_session():
            # Construir la consulta base
            query = select(ReservationModel).where(
                and_(
                    ReservationModel.branch_id == branch_id,
                    # Verificar que haya solapamiento de períodos
                    # Una reserva se solapa si:
                    # - Su start_time es antes del end_time del período buscado Y
                    # - Su end_time es después del start_time del período buscado
                    ReservationModel.start_time < end_time,
                    ReservationModel.end_time > start_time
                )
            )
            
            # Filtrar por estado si se especifica
            if status:
                query = query.where(ReservationModel.status == ReservationStatus(status))
            
            # Ordenar por fecha y hora de inicio
            query = query.order_by(ReservationModel.start_time)
            
            result = await session.execute(query)
            reservation_models = result.scalars().all()
            
            logger.info(f"✅ Se encontraron {len(reservation_models)} reservas en el período")
            
            # Cargar explícitamente las relaciones para cada modelo
            for model in reservation_models:
                await session.refresh(model, attribute_names=['order_numbers'])
            
            return [model.to_domain() for model in reservation_models] 