"""
Implementación del repositorio de estados
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload

from ...domain.entities.state import State
from ...domain.interfaces.state_repository import StateRepository
from ...domain.dto.requests.state_requests import StateFilterRequest
from ..models.state import State as StateModel

class StateRepositoryImpl(StateRepository):
    """Implementación del repositorio de estados"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, state: State) -> State:
        """Crear un estado"""
        state_model = StateModel(
            name=state.name,
            code=state.code,
            country_id=state.country_id,
            is_active=state.is_active
        )
        
        self.session.add(state_model)
        await self.session.commit()
        await self.session.refresh(state_model)
        
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
        """Obtener estado por ID"""
        result = await self.session.execute(
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
        """Obtener estado por código"""
        result = await self.session.execute(
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
    
    async def get_by_country_id(self, country_id: int) -> List[State]:
        """Obtener estados por país"""
        result = await self.session.execute(
            select(StateModel)
            .where(StateModel.country_id == country_id)
            .where(StateModel.is_active == True)
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
    
    async def get_all(self, filter_request: StateFilterRequest) -> tuple[List[State], int]:
        """Obtener todos los estados con filtros y paginación"""
        query = select(StateModel)
        count_query = select(func.count(StateModel.id))
        
        # Aplicar filtros
        if filter_request.name:
            query = query.where(StateModel.name.ilike(f"%{filter_request.name}%"))
            count_query = count_query.where(StateModel.name.ilike(f"%{filter_request.name}%"))
        
        if filter_request.code:
            query = query.where(StateModel.code.ilike(f"%{filter_request.code}%"))
            count_query = count_query.where(StateModel.code.ilike(f"%{filter_request.code}%"))
        
        if filter_request.country_id:
            query = query.where(StateModel.country_id == filter_request.country_id)
            count_query = count_query.where(StateModel.country_id == filter_request.country_id)
        
        if filter_request.is_active is not None:
            query = query.where(StateModel.is_active == filter_request.is_active)
            count_query = count_query.where(StateModel.is_active == filter_request.is_active)
        
        # Obtener total
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Aplicar paginación
        query = query.offset(filter_request.offset).limit(filter_request.limit)
        
        # Ejecutar query
        result = await self.session.execute(query)
        state_models = result.scalars().all()
        
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
    
    async def update(self, state_id: int, state: State) -> Optional[State]:
        """Actualizar un estado"""
        result = await self.session.execute(
            update(StateModel)
            .where(StateModel.id == state_id)
            .values(
                name=state.name,
                code=state.code,
                country_id=state.country_id,
                is_active=state.is_active
            )
        )
        await self.session.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(state_id)
        return None
    
    async def delete(self, state_id: int) -> bool:
        """Eliminar un estado (soft delete)"""
        result = await self.session.execute(
            update(StateModel)
            .where(StateModel.id == state_id)
            .values(is_active=False)
        )
        await self.session.commit()
        
        return result.rowcount > 0
    
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un estado con el código dado"""
        query = select(StateModel).where(StateModel.code == code)
        if exclude_id:
            query = query.where(StateModel.id != exclude_id)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
    
    async def exists_by_id(self, state_id: int) -> bool:
        """Verificar si existe un estado con el ID dado"""
        result = await self.session.execute(
            select(StateModel).where(StateModel.id == state_id)
        )
        return result.scalar_one_or_none() is not None
    
    async def exists_by_country_id(self, country_id: int) -> bool:
        """Verificar si existe un país con el ID dado"""
        result = await self.session.execute(
            select(StateModel).where(StateModel.country_id == country_id)
        )
        return result.scalar_one_or_none() is not None 