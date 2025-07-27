"""
Implementación del repositorio de ciudades
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload

from ...domain.entities.city import City
from ...domain.interfaces.city_repository import CityRepository
from ...domain.dto.requests.city_requests import CityFilterRequest
from ..models.city import City as CityModel
from ..models.state import State as StateModel

class CityRepositoryImpl(CityRepository):
    """Implementación del repositorio de ciudades"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, city: City) -> City:
        """Crear una ciudad"""
        city_model = CityModel(
            name=city.name,
            code=city.code,
            state_id=city.state_id,
            is_active=city.is_active
        )
        
        self.session.add(city_model)
        await self.session.commit()
        await self.session.refresh(city_model)
        
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
        result = await self.session.execute(
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
    
    async def get_by_name(self, name: str) -> Optional[City]:
        """Obtener ciudad por nombre"""
        result = await self.session.execute(
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
        result = await self.session.execute(
            select(CityModel)
            .where(CityModel.state_id == state_id)
            .where(CityModel.is_active == True)
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
        """Obtener ciudades por país (a través del estado)"""
        result = await self.session.execute(
            select(CityModel)
            .join(StateModel, CityModel.state_id == StateModel.id)
            .where(StateModel.country_id == country_id)
            .where(CityModel.is_active == True)
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
    
    async def get_all(self, filter_request: CityFilterRequest) -> tuple[List[City], int]:
        """Obtener todas las ciudades con filtros y paginación"""
        query = select(CityModel)
        count_query = select(func.count(CityModel.id))
        
        # Aplicar filtros
        if filter_request.name:
            query = query.where(CityModel.name.ilike(f"%{filter_request.name}%"))
            count_query = count_query.where(CityModel.name.ilike(f"%{filter_request.name}%"))
        
        if filter_request.state_id:
            query = query.where(CityModel.state_id == filter_request.state_id)
            count_query = count_query.where(CityModel.state_id == filter_request.state_id)
        
        if filter_request.country_id:
            query = query.join(StateModel, CityModel.state_id == StateModel.id)
            query = query.where(StateModel.country_id == filter_request.country_id)
            count_query = count_query.join(StateModel, CityModel.state_id == StateModel.id)
            count_query = count_query.where(StateModel.country_id == filter_request.country_id)
        
        if filter_request.is_active is not None:
            query = query.where(CityModel.is_active == filter_request.is_active)
            count_query = count_query.where(CityModel.is_active == filter_request.is_active)
        
        # Obtener total
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Aplicar paginación
        query = query.offset(filter_request.offset).limit(filter_request.limit)
        
        # Ejecutar query
        result = await self.session.execute(query)
        city_models = result.scalars().all()
        
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
    
    async def update(self, city_id: int, city: City) -> Optional[City]:
        """Actualizar una ciudad"""
        result = await self.session.execute(
            update(CityModel)
            .where(CityModel.id == city_id)
            .values(
                name=city.name,
                code=city.code,
                state_id=city.state_id,
                is_active=city.is_active
            )
        )
        await self.session.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(city_id)
        return None
    
    async def delete(self, city_id: int) -> bool:
        """Eliminar una ciudad (soft delete)"""
        result = await self.session.execute(
            update(CityModel)
            .where(CityModel.id == city_id)
            .values(is_active=False)
        )
        await self.session.commit()
        
        return result.rowcount > 0
    
    async def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe una ciudad con el nombre dado"""
        query = select(CityModel).where(CityModel.name == name)
        if exclude_id:
            query = query.where(CityModel.id != exclude_id)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
    
    async def exists_by_id(self, city_id: int) -> bool:
        """Verificar si existe una ciudad con el ID dado"""
        result = await self.session.execute(
            select(CityModel).where(CityModel.id == city_id)
        )
        return result.scalar_one_or_none() is not None
    
    async def exists_by_state_id(self, state_id: int) -> bool:
        """Verificar si existe un estado con el ID dado"""
        result = await self.session.execute(
            select(CityModel).where(CityModel.state_id == state_id)
        )
        return result.scalar_one_or_none() is not None 