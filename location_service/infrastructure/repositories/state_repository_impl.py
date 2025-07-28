"""
Implementación del repositorio para estados
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ...domain.interfaces.state_repository import StateRepository
from ...domain.entities.state import State
from ...domain.dto.requests.state_requests import StateFilterRequest
from ..models.state import State as StateModel
from commons.database import get_db_session


class StateRepositoryImpl(StateRepository):
    """Implementación del repositorio para estados"""
    
    async def create(self, state: State) -> State:
        """Crear un nuevo estado"""
        async for session in get_db_session():
            # Verificar si ya existe un estado con el mismo código
            if await self.exists_by_code(state.code):
                raise ValueError(f"Ya existe un estado con el código '{state.code}'")
            
            # Crear el modelo
            state_model = StateModel(
                name=state.name,
                code=state.code,
                country_id=state.country_id,
                is_active=state.is_active
            )
            
            session.add(state_model)
            await session.commit()
            await session.refresh(state_model)
            
            # Retornar entidad del dominio
            return State(
                id=state_model.id,
                name=state_model.name,
                code=state_model.code,
                country_id=state_model.country_id,
                is_active=state_model.is_active,
                created_at=state_model.created_at,
                updated_at=state_model.updated_at
            )
    
    async def get_by_id(self, state_id: int) -> Optional[State]:
        """Obtener un estado por ID"""
        async for session in get_db_session():
            result = await session.execute(
                select(StateModel).where(StateModel.id == state_id)
            )
            state_model = result.scalar_one_or_none()
            
            if not state_model:
                return None
            
            return State(
                id=state_model.id,
                name=state_model.name,
                code=state_model.code,
                country_id=state_model.country_id,
                is_active=state_model.is_active,
                created_at=state_model.created_at,
                updated_at=state_model.updated_at
            )
    
    async def get_by_code(self, code: str) -> Optional[State]:
        """Obtener un estado por código"""
        async for session in get_db_session():
            result = await session.execute(
                select(StateModel).where(StateModel.code == code)
            )
            state_model = result.scalar_one_or_none()
            
            if not state_model:
                return None
            
            return State(
                id=state_model.id,
                name=state_model.name,
                code=state_model.code,
                country_id=state_model.country_id,
                is_active=state_model.is_active,
                created_at=state_model.created_at,
                updated_at=state_model.updated_at
            )
    
    async def get_all(self, filter_request: StateFilterRequest) -> Tuple[List[State], int]:
        """Obtener todos los estados con filtros y paginación"""
        async for session in get_db_session():
            query = select(StateModel)
            
            # Aplicar filtros
            if filter_request.name:
                query = query.where(StateModel.name.ilike(f"%{filter_request.name}%"))
            
            if filter_request.code:
                query = query.where(StateModel.code.ilike(f"%{filter_request.code}%"))
            
            if filter_request.country_id:
                query = query.where(StateModel.country_id == filter_request.country_id)
            
            if filter_request.is_active is not None:
                query = query.where(StateModel.is_active == filter_request.is_active)
            
            # Contar total
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await session.execute(count_query)
            total = total_result.scalar()
            
            # Aplicar paginación y ordenamiento
            query = query.offset(filter_request.offset).limit(filter_request.limit).order_by(StateModel.name)
            
            result = await session.execute(query)
            state_models = result.scalars().all()
            
            # Convertir a entidades del dominio
            states = [
                State(
                    id=model.id,
                    name=model.name,
                    code=model.code,
                    country_id=model.country_id,
                    is_active=model.is_active,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in state_models
            ]
            
            return states, total
    
    async def get_by_country_id(self, country_id: int) -> List[State]:
        """Obtener estados por país"""
        async for session in get_db_session():
            result = await session.execute(
                select(StateModel)
                .where(StateModel.country_id == country_id)
                .order_by(StateModel.name)
            )
            state_models = result.scalars().all()
            
            return [
                State(
                    id=model.id,
                    name=model.name,
                    code=model.code,
                    country_id=model.country_id,
                    is_active=model.is_active,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in state_models
            ]
    
    async def exists_by_country_id(self, country_id: int) -> bool:
        """Verificar si existe un país con el ID dado"""
        async for session in get_db_session():
            result = await session.execute(
                select(StateModel).where(StateModel.country_id == country_id)
            )
            return result.scalar_one_or_none() is not None
    
    async def update(self, state_id: int, state: State) -> Optional[State]:
        """Actualizar un estado"""
        async for session in get_db_session():
            result = await session.execute(
                select(StateModel).where(StateModel.id == state_id)
            )
            state_model = result.scalar_one_or_none()
            
            if not state_model:
                return None
            
            # Verificar si ya existe otro estado con el mismo código
            if await self.exists_by_code(state.code, exclude_id=state_id):
                raise ValueError(f"Ya existe un estado con el código '{state.code}'")
            
            # Actualizar campos
            if state.name is not None:
                state_model.name = state.name
            if state.code is not None:
                state_model.code = state.code
            if state.country_id is not None:
                state_model.country_id = state.country_id
            if state.is_active is not None:
                state_model.is_active = state.is_active
            
            await session.commit()
            await session.refresh(state_model)
            
            return State(
                id=state_model.id,
                name=state_model.name,
                code=state_model.code,
                country_id=state_model.country_id,
                is_active=state_model.is_active,
                created_at=state_model.created_at,
                updated_at=state_model.updated_at
            )
    
    async def delete(self, state_id: int) -> bool:
        """Eliminar un estado"""
        async for session in get_db_session():
            result = await session.execute(
                select(StateModel).where(StateModel.id == state_id)
            )
            state_model = result.scalar_one_or_none()
            
            if not state_model:
                return False
            
            await session.delete(state_model)
            await session.commit()
            
            return True
    
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un estado con el código dado"""
        async for session in get_db_session():
            query = select(StateModel).where(StateModel.code == code)
            
            if exclude_id:
                query = query.where(StateModel.id != exclude_id)
            
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None
    
    async def exists_by_id(self, state_id: int) -> bool:
        """Verificar si existe un estado con el ID dado"""
        async for session in get_db_session():
            result = await session.execute(
                select(StateModel).where(StateModel.id == state_id)
            )
            return result.scalar_one_or_none() is not None 