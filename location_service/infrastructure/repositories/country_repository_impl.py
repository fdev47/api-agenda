"""
Implementación del repositorio para países
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.entities.country import Country
from ...domain.dto.requests.country_requests import CountryFilterRequest
from ..models.country import Country as CountryModel
from commons.database import get_db_session


class CountryRepositoryImpl(CountryRepository):
    """Implementación del repositorio para países"""
    
    async def create(self, country: Country) -> Country:
        """Crear un nuevo país"""
        async for session in get_db_session():
            # Verificar si ya existe un país con el mismo código
            if await self.exists_by_code(country.code):
                raise ValueError(f"Ya existe un país con el código '{country.code}'")
            
            # Crear el modelo
            country_model = CountryModel(
                name=country.name,
                code=country.code,
                is_active=country.is_active
            )
            
            session.add(country_model)
            await session.commit()
            await session.refresh(country_model)
            
            # Retornar entidad del dominio
            return Country(
                id=country_model.id,
                name=country_model.name,
                code=country_model.code,
                is_active=country_model.is_active,
                created_at=country_model.created_at,
                updated_at=country_model.updated_at
            )
    
    async def get_by_id(self, country_id: int) -> Optional[Country]:
        """Obtener un país por ID"""
        async for session in get_db_session():
            result = await session.execute(
                select(CountryModel).where(CountryModel.id == country_id)
            )
            country_model = result.scalar_one_or_none()
            
            if not country_model:
                return None
            
            return Country(
                id=country_model.id,
                name=country_model.name,
                code=country_model.code,
                is_active=country_model.is_active,
                created_at=country_model.created_at,
                updated_at=country_model.updated_at
            )
    
    async def get_by_code(self, code: str) -> Optional[Country]:
        """Obtener un país por código"""
        async for session in get_db_session():
            result = await session.execute(
                select(CountryModel).where(CountryModel.code == code)
            )
            country_model = result.scalar_one_or_none()
            
            if not country_model:
                return None
            
            return Country(
                id=country_model.id,
                name=country_model.name,
                code=country_model.code,
                is_active=country_model.is_active,
                created_at=country_model.created_at,
                updated_at=country_model.updated_at
            )
    
    async def get_all(self, filter_request: CountryFilterRequest) -> Tuple[List[Country], int]:
        """Obtener todos los países con filtros y paginación"""
        async for session in get_db_session():
            query = select(CountryModel)
            
            # Aplicar filtros
            if filter_request.name:
                query = query.where(CountryModel.name.ilike(f"%{filter_request.name}%"))
            
            if filter_request.code:
                query = query.where(CountryModel.code.ilike(f"%{filter_request.code}%"))
            
            if filter_request.is_active is not None:
                query = query.where(CountryModel.is_active == filter_request.is_active)
            
            # Contar total
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await session.execute(count_query)
            total = total_result.scalar()
            
            # Aplicar paginación y ordenamiento
            query = query.offset(filter_request.offset).limit(filter_request.limit).order_by(CountryModel.name)
            
            result = await session.execute(query)
            country_models = result.scalars().all()
            
            # Convertir a entidades del dominio
            countries = [
                Country(
                    id=model.id,
                    name=model.name,
                    code=model.code,
                    is_active=model.is_active,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in country_models
            ]
            
            return countries, total
    
    async def update(self, country_id: int, country: Country) -> Optional[Country]:
        """Actualizar un país"""
        async for session in get_db_session():
            result = await session.execute(
                select(CountryModel).where(CountryModel.id == country_id)
            )
            country_model = result.scalar_one_or_none()
            
            if not country_model:
                return None
            
            # Verificar si ya existe otro país con el mismo código
            if await self.exists_by_code(country.code, exclude_id=country_id):
                raise ValueError(f"Ya existe un país con el código '{country.code}'")
            
            # Actualizar campos
            if country.name is not None:
                country_model.name = country.name
            if country.code is not None:
                country_model.code = country.code
            if country.is_active is not None:
                country_model.is_active = country.is_active
            
            await session.commit()
            await session.refresh(country_model)
            
            return Country(
                id=country_model.id,
                name=country_model.name,
                code=country_model.code,
                is_active=country_model.is_active,
                created_at=country_model.created_at,
                updated_at=country_model.updated_at
            )
    
    async def delete(self, country_id: int) -> bool:
        """Eliminar un país"""
        async for session in get_db_session():
            result = await session.execute(
                select(CountryModel).where(CountryModel.id == country_id)
            )
            country_model = result.scalar_one_or_none()
            
            if not country_model:
                return False
            
            await session.delete(country_model)
            await session.commit()
            
            return True
    
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un país con el código dado"""
        async for session in get_db_session():
            query = select(CountryModel).where(CountryModel.code == code)
            
            if exclude_id:
                query = query.where(CountryModel.id != exclude_id)
            
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None
    
    async def exists_by_id(self, country_id: int) -> bool:
        """Verificar si existe un país con el ID dado"""
        async for session in get_db_session():
            result = await session.execute(
                select(CountryModel).where(CountryModel.id == country_id)
            )
            return result.scalar_one_or_none() is not None 