"""
Implementación del repositorio para ciudades
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ...domain.entities.city import City
from ...domain.interfaces.city_repository import CityRepository
from ...domain.dto.requests.city_requests import CityFilterRequest
from ..models.city import City as CityModel
from ..models.state import State as StateModel
from commons.database import get_db_session

class CityRepositoryImpl(CityRepository):
    """Implementación del repositorio de ciudades"""
    
    async def create(self, city: City) -> City:
        """Crear una ciudad"""
        async for session in get_db_session():
            city_model = CityModel(
                name=city.name,
                code=city.code,
                state_id=city.state_id,
                is_active=city.is_active
            )
            
            session.add(city_model)
            await session.commit()
            await session.refresh(city_model)
            
            return City(
                id=city_model.id,
                name=city_model.name,
                code=city_model.code,
                state_id=city_model.state_id,
                is_active=city_model.is_active,
                created_at=city_model.created_at,
                updated_at=city_model.updated_at
            )
    
    async def get_by_id(self, city_id: int) -> Optional[City]:
        """Obtener ciudad por ID"""
        async for session in get_db_session():
            result = await session.execute(
                select(CityModel).where(CityModel.id == city_id)
            )
            city_model = result.scalar_one_or_none()
            
            if not city_model:
                return None
                
            return City(
                id=city_model.id,
                name=city_model.name,
                code=city_model.code,
                state_id=city_model.state_id,
                is_active=city_model.is_active,
                created_at=city_model.created_at,
                updated_at=city_model.updated_at
            )
    
    async def get_all(self, filter_request: CityFilterRequest) -> Tuple[List[City], int]:
        """Obtener todas las ciudades con filtros y paginación"""
        async for session in get_db_session():
            query = select(CityModel)
            
            # Aplicar filtros
            if filter_request.name:
                query = query.where(CityModel.name.ilike(f"%{filter_request.name}%"))
            
            if filter_request.code:
                query = query.where(CityModel.code.ilike(f"%{filter_request.code}%"))
            
            if filter_request.state_id:
                query = query.where(CityModel.state_id == filter_request.state_id)
            
            if filter_request.is_active is not None:
                query = query.where(CityModel.is_active == filter_request.is_active)
            
            # Contar total
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await session.execute(count_query)
            total = total_result.scalar()
            
            # Aplicar paginación y ordenamiento
            query = query.offset(filter_request.offset).limit(filter_request.limit).order_by(CityModel.name)
            
            result = await session.execute(query)
            city_models = result.scalars().all()
            
            # Convertir a entidades del dominio
            cities = [
                City(
                    id=model.id,
                    name=model.name,
                    code=model.code,
                    state_id=model.state_id,
                    is_active=model.is_active,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in city_models
            ]
            
            return cities, total
    
    async def get_by_name(self, name: str) -> Optional[City]:
        """Obtener ciudad por nombre"""
        async for session in get_db_session():
            result = await session.execute(
                select(CityModel).where(CityModel.name == name)
            )
            city_model = result.scalar_one_or_none()
            
            if not city_model:
                return None
            
            return City(
                id=city_model.id,
                name=city_model.name,
                code=city_model.code,
                state_id=city_model.state_id,
                is_active=city_model.is_active,
                created_at=city_model.created_at,
                updated_at=city_model.updated_at
            )
    
    async def get_by_state_id(self, state_id: int) -> List[City]:
        """Obtener ciudades por estado"""
        async for session in get_db_session():
            result = await session.execute(
                select(CityModel)
                .where(CityModel.state_id == state_id)
                .order_by(CityModel.name)
            )
            city_models = result.scalars().all()
            
            return [
                City(
                    id=model.id,
                    name=model.name,
                    code=model.code,
                    state_id=model.state_id,
                    is_active=model.is_active,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in city_models
            ]
    
    async def get_by_country_id(self, country_id: int) -> List[City]:
        """Obtener ciudades por país"""
        async for session in get_db_session():
            result = await session.execute(
                select(CityModel)
                .join(StateModel, CityModel.state_id == StateModel.id)
                .where(StateModel.country_id == country_id)
                .order_by(CityModel.name)
            )
            city_models = result.scalars().all()
            
            return [
                City(
                    id=model.id,
                    name=model.name,
                    code=model.code,
                    state_id=model.state_id,
                    is_active=model.is_active,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in city_models
            ]
    
    async def update(self, city_id: int, city: City) -> Optional[City]:
        """Actualizar una ciudad"""
        async for session in get_db_session():
            result = await session.execute(
                select(CityModel).where(CityModel.id == city_id)
            )
            city_model = result.scalar_one_or_none()
            
            if not city_model:
                return None
            
            # Actualizar campos
            city_model.name = city.name
            city_model.code = city.code
            city_model.state_id = city.state_id
            city_model.is_active = city.is_active
            
            await session.commit()
            await session.refresh(city_model)
            
            return City(
                id=city_model.id,
                name=city_model.name,
                code=city_model.code,
                state_id=city_model.state_id,
                is_active=city_model.is_active,
                created_at=city_model.created_at,
                updated_at=city_model.updated_at
            )
    
    async def delete(self, city_id: int) -> bool:
        """Eliminar una ciudad (soft delete)"""
        async for session in get_db_session():
            result = await session.execute(
                select(CityModel).where(CityModel.id == city_id)
            )
            city_model = result.scalar_one_or_none()
            
            if not city_model:
                return False
            
            city_model.is_active = False
            await session.commit()
            
            return True
    
    async def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe una ciudad con el nombre dado"""
        async for session in get_db_session():
            query = select(CityModel).where(CityModel.name == name)
            
            if exclude_id:
                query = query.where(CityModel.id != exclude_id)
            
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None
    
    async def exists_by_id(self, city_id: int) -> bool:
        """Verificar si existe una ciudad con el ID dado"""
        async for session in get_db_session():
            result = await session.execute(
                select(CityModel).where(CityModel.id == city_id)
            )
            return result.scalar_one_or_none() is not None
    
    async def exists_by_state_id(self, state_id: int) -> bool:
        """Verificar si existe un estado con el ID dado"""
        async for session in get_db_session():
            result = await session.execute(
                select(CityModel).where(CityModel.state_id == state_id)
            )
            return result.scalar_one_or_none() is not None 