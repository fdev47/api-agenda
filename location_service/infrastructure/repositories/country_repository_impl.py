"""
Implementación del repositorio de países
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload

from ...domain.entities.country import Country
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.dto.requests.country_requests import CountryFilterRequest
from ..models.country import Country as CountryModel

class CountryRepositoryImpl(CountryRepository):
    """Implementación del repositorio de países"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, country: Country) -> Country:
        """Crear un país"""
        country_model = CountryModel(
            name=country.name,
            code=country.code,
            phone_code=country.phone_code,
            is_active=country.is_active
        )
        
        self.session.add(country_model)
        await self.session.commit()
        await self.session.refresh(country_model)
        
        return Country(
            id=country_model.id,
            name=country_model.name,
            code=country_model.code,
            phone_code=country_model.phone_code,
            is_active=country_model.is_active,
            created_at=country_model.created_at,
            updated_at=country_model.updated_at
        )
    
    async def get_by_id(self, country_id: int) -> Optional[Country]:
        """Obtener país por ID"""
        result = await self.session.execute(
            select(CountryModel).where(CountryModel.id == country_id)
        )
        country_model = result.scalar_one_or_none()
        
        if not country_model:
            return None
            
        return Country(
            id=country_model.id,
            name=country_model.name,
            code=country_model.code,
            phone_code=country_model.phone_code,
            is_active=country_model.is_active,
            created_at=country_model.created_at,
            updated_at=country_model.updated_at
        )
    
    async def get_by_code(self, code: str) -> Optional[Country]:
        """Obtener país por código ISO"""
        result = await self.session.execute(
            select(CountryModel).where(CountryModel.code == code)
        )
        country_model = result.scalar_one_or_none()
        
        if not country_model:
            return None
            
        return Country(
            id=country_model.id,
            name=country_model.name,
            code=country_model.code,
            phone_code=country_model.phone_code,
            is_active=country_model.is_active,
            created_at=country_model.created_at,
            updated_at=country_model.updated_at
        )
    
    async def get_all(self, filter_request: CountryFilterRequest) -> tuple[List[Country], int]:
        """Obtener todos los países con filtros y paginación"""
        query = select(CountryModel)
        count_query = select(func.count(CountryModel.id))
        
        # Aplicar filtros
        if filter_request.name:
            query = query.where(CountryModel.name.ilike(f"%{filter_request.name}%"))
            count_query = count_query.where(CountryModel.name.ilike(f"%{filter_request.name}%"))
        
        if filter_request.code:
            query = query.where(CountryModel.code.ilike(f"%{filter_request.code}%"))
            count_query = count_query.where(CountryModel.code.ilike(f"%{filter_request.code}%"))
        
        if filter_request.is_active is not None:
            query = query.where(CountryModel.is_active == filter_request.is_active)
            count_query = count_query.where(CountryModel.is_active == filter_request.is_active)
        
        # Obtener total
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Aplicar paginación
        query = query.offset(filter_request.offset).limit(filter_request.limit)
        
        # Ejecutar query
        result = await self.session.execute(query)
        country_models = result.scalars().all()
        
        countries = [
            Country(
                id=model.id,
                name=model.name,
                code=model.code,
                phone_code=model.phone_code,
                is_active=model.is_active,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in country_models
        ]
        
        return countries, total
    
    async def update(self, country_id: int, country: Country) -> Optional[Country]:
        """Actualizar un país"""
        result = await self.session.execute(
            update(CountryModel)
            .where(CountryModel.id == country_id)
            .values(
                name=country.name,
                code=country.code,
                phone_code=country.phone_code,
                is_active=country.is_active
            )
        )
        await self.session.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(country_id)
        return None
    
    async def delete(self, country_id: int) -> bool:
        """Eliminar un país (soft delete)"""
        result = await self.session.execute(
            update(CountryModel)
            .where(CountryModel.id == country_id)
            .values(is_active=False)
        )
        await self.session.commit()
        
        return result.rowcount > 0
    
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un país con el código dado"""
        query = select(CountryModel).where(CountryModel.code == code)
        if exclude_id:
            query = query.where(CountryModel.id != exclude_id)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
    
    async def exists_by_id(self, country_id: int) -> bool:
        """Verificar si existe un país con el ID dado"""
        result = await self.session.execute(
            select(CountryModel).where(CountryModel.id == country_id)
        )
        return result.scalar_one_or_none() is not None 