"""
Implementación del repositorio para horarios de rampas
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from ...domain.interfaces.ramp_schedule_repository import RampScheduleRepository
from ...domain.entities.ramp_schedule import RampSchedule
from ...domain.entities.day_of_week import DayOfWeek
from ...domain.dto.requests.ramp_schedule_requests import RampScheduleFilterRequest
from ..models.ramp_schedule import RampSchedule as RampScheduleModel
from commons.database import get_db_session


class RampScheduleRepositoryImpl(RampScheduleRepository):
    """Implementación del repositorio para horarios de rampas"""
    
    async def create(self, schedule: RampSchedule) -> RampSchedule:
        """Crear un nuevo horario"""
        async for session in get_db_session():
            # Crear el modelo
            schedule_model = RampScheduleModel(
                ramp_id=schedule.ramp_id,
                day_of_week=schedule.day_of_week,
                name=schedule.name,
                start_time=schedule.start_time,
                end_time=schedule.end_time,
                is_active=schedule.is_active
            )
            
            session.add(schedule_model)
            await session.commit()
            await session.refresh(schedule_model)
            
            # Retornar entidad del dominio
            return RampSchedule(
                id=schedule_model.id,
                ramp_id=schedule_model.ramp_id,
                day_of_week=schedule_model.day_of_week,
                name=schedule_model.name,
                start_time=schedule_model.start_time,
                end_time=schedule_model.end_time,
                is_active=schedule_model.is_active,
                created_at=schedule_model.created_at,
                updated_at=schedule_model.updated_at
            )
    
    async def get_by_id(self, schedule_id: int) -> Optional[RampSchedule]:
        """Obtener un horario por ID"""
        async for session in get_db_session():
            query = select(RampScheduleModel).where(RampScheduleModel.id == schedule_id)
            result = await session.execute(query)
            schedule_model = result.scalar_one_or_none()
            
            if not schedule_model:
                return None
            
            return RampSchedule(
                id=schedule_model.id,
                ramp_id=schedule_model.ramp_id,
                day_of_week=schedule_model.day_of_week,
                name=schedule_model.name,
                start_time=schedule_model.start_time,
                end_time=schedule_model.end_time,
                is_active=schedule_model.is_active,
                created_at=schedule_model.created_at,
                updated_at=schedule_model.updated_at
            )
    
    async def get_by_ramp_id(self, ramp_id: int) -> List[RampSchedule]:
        """Obtener todos los horarios de una rampa"""
        async for session in get_db_session():
            query = select(RampScheduleModel).where(
                RampScheduleModel.ramp_id == ramp_id
            ).order_by(RampScheduleModel.day_of_week, RampScheduleModel.start_time)
            
            result = await session.execute(query)
            schedule_models = result.scalars().all()
            
            return [
                RampSchedule(
                    id=schedule_model.id,
                    ramp_id=schedule_model.ramp_id,
                    day_of_week=schedule_model.day_of_week,
                    name=schedule_model.name,
                    start_time=schedule_model.start_time,
                    end_time=schedule_model.end_time,
                    is_active=schedule_model.is_active,
                    created_at=schedule_model.created_at,
                    updated_at=schedule_model.updated_at
                )
                for schedule_model in schedule_models
            ]
    
    async def get_by_ramp_and_day(self, ramp_id: int, day_of_week: int) -> List[RampSchedule]:
        """Obtener horarios de una rampa para un día específico"""
        async for session in get_db_session():
            query = select(RampScheduleModel).where(
                and_(
                    RampScheduleModel.ramp_id == ramp_id,
                    RampScheduleModel.day_of_week == day_of_week
                )
            ).order_by(RampScheduleModel.start_time)
            
            result = await session.execute(query)
            schedule_models = result.scalars().all()
            
            return [
                RampSchedule(
                    id=schedule_model.id,
                    ramp_id=schedule_model.ramp_id,
                    day_of_week=schedule_model.day_of_week,
                    name=schedule_model.name,
                    start_time=schedule_model.start_time,
                    end_time=schedule_model.end_time,
                    is_active=schedule_model.is_active,
                    created_at=schedule_model.created_at,
                    updated_at=schedule_model.updated_at
                )
                for schedule_model in schedule_models
            ]
    
    async def list(self, filter_request: RampScheduleFilterRequest) -> Tuple[List[RampSchedule], int]:
        """Listar horarios con filtros y paginación"""
        async for session in get_db_session():
            # Construir query base
            query = select(RampScheduleModel)
            count_query = select(func.count(RampScheduleModel.id))
            
            # Aplicar filtros
            filters = []
            
            if filter_request.ramp_id is not None:
                filters.append(RampScheduleModel.ramp_id == filter_request.ramp_id)
            
            if filter_request.day_of_week is not None:
                filters.append(RampScheduleModel.day_of_week == filter_request.day_of_week)
            
            if filter_request.name is not None:
                filters.append(RampScheduleModel.name.ilike(f"%{filter_request.name}%"))
            
            if filter_request.is_active is not None:
                filters.append(RampScheduleModel.is_active == filter_request.is_active)
            
            if filters:
                query = query.where(and_(*filters))
                count_query = count_query.where(and_(*filters))
            
            # Obtener total
            count_result = await session.execute(count_query)
            total = count_result.scalar()
            
            # Aplicar ordenamiento y paginación
            query = query.order_by(
                RampScheduleModel.ramp_id,
                RampScheduleModel.day_of_week,
                RampScheduleModel.start_time
            ).limit(filter_request.limit).offset(filter_request.offset)
            
            # Ejecutar query
            result = await session.execute(query)
            schedule_models = result.scalars().all()
            
            schedules = [
                RampSchedule(
                    id=schedule_model.id,
                    ramp_id=schedule_model.ramp_id,
                    day_of_week=schedule_model.day_of_week,
                    name=schedule_model.name,
                    start_time=schedule_model.start_time,
                    end_time=schedule_model.end_time,
                    is_active=schedule_model.is_active,
                    created_at=schedule_model.created_at,
                    updated_at=schedule_model.updated_at
                )
                for schedule_model in schedule_models
            ]
            
            return schedules, total
    
    async def update(self, schedule: RampSchedule) -> RampSchedule:
        """Actualizar un horario"""
        async for session in get_db_session():
            query = select(RampScheduleModel).where(RampScheduleModel.id == schedule.id)
            result = await session.execute(query)
            schedule_model = result.scalar_one_or_none()
            
            if not schedule_model:
                raise ValueError(f"Horario con ID {schedule.id} no encontrado")
            
            # Actualizar campos
            schedule_model.ramp_id = schedule.ramp_id
            schedule_model.day_of_week = schedule.day_of_week
            schedule_model.name = schedule.name
            schedule_model.start_time = schedule.start_time
            schedule_model.end_time = schedule.end_time
            schedule_model.is_active = schedule.is_active
            
            await session.commit()
            await session.refresh(schedule_model)
            
            return RampSchedule(
                id=schedule_model.id,
                ramp_id=schedule_model.ramp_id,
                day_of_week=schedule_model.day_of_week,
                name=schedule_model.name,
                start_time=schedule_model.start_time,
                end_time=schedule_model.end_time,
                is_active=schedule_model.is_active,
                created_at=schedule_model.created_at,
                updated_at=schedule_model.updated_at
            )
    
    async def delete(self, schedule_id: int) -> bool:
        """Eliminar un horario"""
        async for session in get_db_session():
            query = select(RampScheduleModel).where(RampScheduleModel.id == schedule_id)
            result = await session.execute(query)
            schedule_model = result.scalar_one_or_none()
            
            if not schedule_model:
                return False
            
            await session.delete(schedule_model)
            await session.commit()
            
            return True

