"""
Implementación del repositorio de horarios
"""
from typing import List, Optional
from datetime import date, datetime, time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
import logging

from ...domain.entities.branch_schedule import BranchSchedule
from ...domain.entities.day_of_week import DayOfWeek
from ...domain.entities.time_slot import TimeSlot
from ...domain.entities.reservation import Reservation
from ...domain.interfaces.schedule_repository import ScheduleRepository
from ...infrastructure.models.schedule import BranchScheduleModel
from ...infrastructure.models.reservation import ReservationModel
from commons.database import get_db_session

# Configurar logging
logger = logging.getLogger(__name__)


class ScheduleRepositoryImpl(ScheduleRepository):
    """Implementación del repositorio de horarios de sucursales"""
    
    def __init__(self):
        pass
    
    async def create(self, schedule: BranchSchedule) -> BranchSchedule:
        """Crear un nuevo horario de sucursal"""
        async for session in get_db_session():
            schedule_model = BranchScheduleModel.from_domain(schedule)
            session.add(schedule_model)
            await session.flush()
            await session.commit()
            await session.refresh(schedule_model)
            
            return schedule_model.to_domain()
    
    async def get_by_id(self, schedule_id: int) -> Optional[BranchSchedule]:
        """Obtener un horario por ID"""
        async for session in get_db_session():
            stmt = select(BranchScheduleModel).where(BranchScheduleModel.id == schedule_id)
            result = await session.execute(stmt)
            schedule_model = result.scalar_one_or_none()
            
            return schedule_model.to_domain() if schedule_model else None
    
    async def get_by_branch_and_day(self, branch_id: int, day_of_week: DayOfWeek) -> Optional[BranchSchedule]:
        """Obtener horario de una sucursal para un día específico"""
        logger.info(f"🔄 Buscando horario para branch_id: {branch_id}, day_of_week: {day_of_week}")
        
        try:
            async for session in get_db_session():
                logger.info("📝 Ejecutando consulta en base de datos...")
                stmt = select(BranchScheduleModel).where(
                    and_(
                        BranchScheduleModel.branch_id == branch_id,
                        BranchScheduleModel.day_of_week == day_of_week
                    )
                )
                logger.info(f"📝 Query: {stmt}")
                
                result = await session.execute(stmt)
                schedule_model = result.scalar_one_or_none()
                
                if schedule_model:
                    logger.info(f"✅ Horario encontrado: id={schedule_model.id}, start_time={schedule_model.start_time}, end_time={schedule_model.end_time}")
                    return schedule_model.to_domain()
                else:
                    logger.warning(f"⚠️ No se encontró horario para branch_id: {branch_id}, day_of_week: {day_of_week}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Error en get_by_branch_and_day: {str(e)}", exc_info=True)
            raise
    
    async def list_by_branch(self, branch_id: int, day_of_week: Optional[DayOfWeek] = None, 
                           is_active: Optional[bool] = None) -> List[BranchSchedule]:
        """Listar horarios de una sucursal con filtros opcionales"""
        async for session in get_db_session():
            conditions = [BranchScheduleModel.branch_id == branch_id]
            
            if day_of_week is not None:
                conditions.append(BranchScheduleModel.day_of_week == day_of_week)
            
            if is_active is not None:
                conditions.append(BranchScheduleModel.is_active == is_active)
            
            stmt = select(BranchScheduleModel).where(and_(*conditions))
            result = await session.execute(stmt)
            schedule_models = result.scalars().all()
            
            return [model.to_domain() for model in schedule_models]
    
    async def update(self, schedule_id: int, schedule_data: dict) -> Optional[BranchSchedule]:
        """Actualizar un horario existente"""
        async for session in get_db_session():
            stmt = select(BranchScheduleModel).where(BranchScheduleModel.id == schedule_id)
            result = await session.execute(stmt)
            schedule_model = result.scalar_one_or_none()
            
            if not schedule_model:
                return None
            
            # Actualizar campos
            for key, value in schedule_data.items():
                if hasattr(schedule_model, key):
                    setattr(schedule_model, key, value)
            
            schedule_model.updated_at = datetime.utcnow()
            await session.flush()
            await session.refresh(schedule_model)
            
            return schedule_model.to_domain()
    
    async def delete(self, schedule_id: int) -> bool:
        """Eliminar un horario"""
        async for session in get_db_session():
            stmt = select(BranchScheduleModel).where(BranchScheduleModel.id == schedule_id)
            result = await session.execute(stmt)
            schedule_model = result.scalar_one_or_none()
            
            if not schedule_model:
                return False
            
            await session.delete(schedule_model)
            return True
    
    async def exists_by_branch_and_day(self, branch_id: int, day_of_week: DayOfWeek, 
                                     exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un horario para una sucursal y día"""
        async for session in get_db_session():
            conditions = [
                BranchScheduleModel.branch_id == branch_id,
                BranchScheduleModel.day_of_week == day_of_week
            ]
            
            if exclude_id:
                conditions.append(BranchScheduleModel.id != exclude_id)
            
            stmt = select(BranchScheduleModel).where(and_(*conditions))
            result = await session.execute(stmt)
            return result.scalar_one_or_none() is not None
    
    async def get_available_slots(self, branch_id: int, target_date: date) -> List[TimeSlot]:
        """Obtener slots disponibles para una fecha específica"""
        # Obtener el día de la semana
        day_of_week_number = target_date.isoweekday()
        day_of_week = DayOfWeek(day_of_week_number)
        
        # Obtener el horario configurado
        schedule = await self.get_by_branch_and_day(branch_id, day_of_week)
        if not schedule or not schedule.is_active:
            return []
        
        # Generar slots base
        base_slots = schedule.generate_time_slots()
        
        # Obtener reservas existentes para esa fecha
        existing_reservations = await self.get_reservations_for_date(branch_id, target_date)
        
        # Marcar slots ocupados
        for slot in base_slots:
            for reservation in existing_reservations:
                reservation_start = datetime.strptime(reservation.schedule_start_time, "%H:%M").time()
                reservation_end = datetime.strptime(reservation.schedule_end_time, "%H:%M").time()
                
                # Verificar si hay solapamiento
                if (slot.start_time < reservation_end and slot.end_time > reservation_start):
                    slot.is_available = False
                    slot.reservation_id = reservation.id
                    break
        
        return base_slots
    
    async def check_slot_availability(self, branch_id: int, target_date: date, 
                                    start_time: str, end_time: str) -> bool:
        """Verificar si un slot específico está disponible"""
        # Obtener slots disponibles
        available_slots = await self.get_available_slots(branch_id, target_date)
        
        # Convertir tiempos de string a time
        start_time_obj = datetime.strptime(start_time, "%H:%M").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M").time()
        
        # Verificar si el slot solicitado está disponible
        for slot in available_slots:
            if (slot.start_time <= start_time_obj and slot.end_time >= end_time_obj and slot.is_available):
                return True
        
        return False
    
    async def get_reservations_for_date(self, branch_id: int, target_date: date) -> List[Reservation]:
        """Obtener reservas existentes para una fecha específica"""
        stmt = select(ReservationModel).where(
            and_(
                ReservationModel.branch_data.contains({"id": branch_id}),
                ReservationModel.schedule_date == target_date,
                ReservationModel.status.in_(["CONFIRMED", "PENDING"])
            )
        )
        result = await self.session.execute(stmt)
        reservation_models = result.scalars().all()
        
        return [model.to_domain() for model in reservation_models] 