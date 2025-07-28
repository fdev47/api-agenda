"""
Implementación del repositorio de reservas
"""
from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from ...domain.entities.reservation import Reservation
from ...domain.entities.reservation_status import ReservationStatus
from ...domain.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...infrastructure.models.reservation import ReservationModel, ReservationOrderNumberModel
from ...domain.exceptions import ReservationNotFoundException
from commons.database import get_db_session


class ReservationRepositoryImpl(ReservationRepository):
    """Implementación del repositorio para reservas"""
    
    def __init__(self):
        pass
    
    async def create(self, reservation: Reservation) -> Reservation:
        """Crear una nueva reserva"""
        async for session in get_db_session():
            # Convertir entidad de dominio a modelo de BD
            reservation_model = ReservationModel.from_domain(reservation)
            
            # Agregar números de pedido
            for order in reservation.order_numbers:
                order_model = ReservationOrderNumberModel(
                    code=order.code,
                    description=order.description
                )
                reservation_model.order_numbers.append(order_model)
            
            await session.add(reservation_model)
            await session.commit()
            await session.refresh(reservation_model)
            
            # Retornar entidad de dominio
            return reservation_model.to_domain()
    
    async def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """Obtener una reserva por ID"""
        async for session in get_db_session():
            result = await session.execute(
                select(ReservationModel).where(ReservationModel.id == reservation_id)
            )
            reservation_model = result.scalar_one_or_none()
            
            if not reservation_model:
                return None
            
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
            
            if filter_request.sector_name:
                conditions.append(ReservationModel.sector_data['name'].astext.ilike(f"%{filter_request.sector_name}%"))
            
            if filter_request.customer_name:
                conditions.append(ReservationModel.customer_data['name'].astext.ilike(f"%{filter_request.customer_name}%"))
            
            if filter_request.customer_email:
                conditions.append(ReservationModel.customer_data['email'].astext.ilike(f"%{filter_request.customer_email}%"))
            
            if filter_request.reservation_date_from:
                conditions.append(ReservationModel.reservation_date >= filter_request.reservation_date_from)
            
            if filter_request.reservation_date_to:
                conditions.append(ReservationModel.reservation_date <= filter_request.reservation_date_to)
            
            if filter_request.status:
                conditions.append(ReservationModel.status == ReservationStatus(filter_request.status))
            
            if filter_request.order_code:
                # Para el filtro de order_code necesitamos hacer un join
                query = query.join(ReservationOrderNumberModel)
                conditions.append(ReservationOrderNumberModel.code.ilike(f"%{filter_request.order_code}%"))
            
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
            
            reservations = [model.to_domain() for model in reservation_models]
            
            return reservations, total
    
    async def update(self, reservation: Reservation) -> Reservation:
        """Actualizar una reserva"""
        reservation_model = self.session.query(ReservationModel).filter(
            ReservationModel.id == reservation.id
        ).first()
        
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
        reservation_model.reservation_date = reservation.reservation_date
        reservation_model.start_time = reservation.start_time
        reservation_model.end_time = reservation.end_time
        reservation_model.status = reservation.status
        reservation_model.notes = reservation.notes
        
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
            "city_name": reservation.branch_data.city_name
        }
        
        reservation_model.sector_data = {
            "sector_id": reservation.sector_data.sector_id,
            "name": reservation.sector_data.name,
            "description": reservation.sector_data.description,
            "sector_type_id": reservation.sector_data.sector_type_id,
            "sector_type_name": reservation.sector_data.sector_type_name,
            "measurement_unit": reservation.sector_data.measurement_unit
        }
        
        reservation_model.customer_data = {
            "customer_id": reservation.customer_data.customer_id,
            "ruc": reservation.customer_data.ruc,
            "company_name": reservation.customer_data.company_name,
            "phone_number": reservation.customer_data.phone_number
        }
        
        # Actualizar números de pedido (eliminar existentes y agregar nuevos)
        self.session.query(ReservationOrderNumberModel).filter(
            ReservationOrderNumberModel.reservation_id == reservation.id
        ).delete()
        
        for order in reservation.order_numbers:
            order_model = ReservationOrderNumberModel(
                reservation_id=reservation.id,
                code=order.code,
                description=order.description
            )
            self.session.add(order_model)
        
        self.session.commit()
        self.session.refresh(reservation_model)
        
        return reservation_model.to_domain()
    
    async def delete(self, reservation_id: int) -> bool:
        """Eliminar una reserva"""
        reservation_model = self.session.query(ReservationModel).filter(
            ReservationModel.id == reservation_id
        ).first()
        
        if not reservation_model:
            return False
        
        self.session.delete(reservation_model)
        self.session.commit()
        
        return True
    
    async def exists_conflict(self, branch_id: int, sector_id: int, start_time: datetime, end_time: datetime, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un conflicto de horario"""
        query = self.session.query(ReservationModel).filter(
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
            query = query.filter(ReservationModel.id != exclude_id)
        
        return query.first() is not None
    
    async def check_conflicts(self, branch_id: int, sector_id: int, start_time: datetime, end_time: datetime, exclude_reservation_id: Optional[int] = None) -> List[Reservation]:
        """Verificar conflictos de horario y retornar las reservas que causan conflicto"""
        query = self.session.query(ReservationModel).filter(
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
            query = query.filter(ReservationModel.id != exclude_reservation_id)
        
        reservation_models = query.all()
        
        return [model.to_domain() for model in reservation_models]
    
    async def get_conflicting_reservation(self, branch_id: int, sector_id: int, start_time: datetime, end_time: datetime, exclude_id: Optional[int] = None) -> Optional[Reservation]:
        """Obtener la reserva que causa conflicto de horario"""
        query = self.session.query(ReservationModel).filter(
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
            query = query.filter(ReservationModel.id != exclude_id)
        
        reservation_model = query.first()
        
        if not reservation_model:
            return None
        
        return reservation_model.to_domain()
    
    async def get_by_user_id(self, user_id: int, limit: int = 10) -> List[Reservation]:
        """Obtener reservas por usuario"""
        reservation_models = self.session.query(ReservationModel).filter(
            ReservationModel.user_id == user_id
        ).order_by(ReservationModel.reservation_date.desc(), ReservationModel.start_time.desc()).limit(limit).all()
        
        return [model.to_domain() for model in reservation_models]
    
    async def get_by_customer_id(self, customer_id: int, limit: int = 10) -> List[Reservation]:
        """Obtener reservas por cliente"""
        reservation_models = self.session.query(ReservationModel).filter(
            ReservationModel.customer_id == customer_id
        ).order_by(ReservationModel.reservation_date.desc(), ReservationModel.start_time.desc()).limit(limit).all()
        
        return [model.to_domain() for model in reservation_models]
    
    async def get_by_branch_id(self, branch_id: int, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> List[Reservation]:
        """Obtener reservas por sucursal"""
        query = self.session.query(ReservationModel).filter(
            ReservationModel.branch_id == branch_id
        )
        
        if date_from:
            query = query.filter(ReservationModel.reservation_date >= date_from)
        
        if date_to:
            query = query.filter(ReservationModel.reservation_date <= date_to)
        
        reservation_models = query.order_by(ReservationModel.reservation_date, ReservationModel.start_time).all()
        
        return [model.to_domain() for model in reservation_models]
    
    async def get_by_sector_id(self, sector_id: int, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> List[Reservation]:
        """Obtener reservas por sector"""
        query = self.session.query(ReservationModel).filter(
            ReservationModel.sector_id == sector_id
        )
        
        if date_from:
            query = query.filter(ReservationModel.reservation_date >= date_from)
        
        if date_to:
            query = query.filter(ReservationModel.reservation_date <= date_to)
        
        reservation_models = query.order_by(ReservationModel.reservation_date, ReservationModel.start_time).all()
        
        return [model.to_domain() for model in reservation_models]
    
    async def get_active_reservations(self, branch_id: Optional[int] = None, sector_id: Optional[int] = None) -> List[Reservation]:
        """Obtener reservas activas (pendientes o confirmadas)"""
        query = self.session.query(ReservationModel).filter(
            ReservationModel.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED])
        )
        
        if branch_id:
            query = query.filter(ReservationModel.branch_id == branch_id)
        
        if sector_id:
            query = query.filter(ReservationModel.sector_id == sector_id)
        
        reservation_models = query.order_by(ReservationModel.reservation_date, ReservationModel.start_time).all()
        
        return [model.to_domain() for model in reservation_models]
    
    async def update_status(self, reservation_id: int, status: str) -> bool:
        """Actualizar solo el estado de una reserva"""
        reservation_model = self.session.query(ReservationModel).filter(
            ReservationModel.id == reservation_id
        ).first()
        
        if not reservation_model:
            return False
        
        reservation_model.status = ReservationStatus(status)
        reservation_model.updated_at = datetime.utcnow()
        
        self.session.commit()
        
        return True 