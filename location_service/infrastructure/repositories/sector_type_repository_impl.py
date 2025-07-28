"""
Implementación del repositorio para tipos de sector
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ...domain.interfaces.sector_type_repository import SectorTypeRepository
from ...domain.entities.sector_type import SectorType
from ...domain.dto.requests.sector_type_requests import SectorTypeFilterRequest
from ...domain.exceptions import SectorTypeNotFoundException, SectorTypeAlreadyExistsException
from ..models.sector_type import SectorType as SectorTypeModel
from commons.database import get_db_session


class SectorTypeRepositoryImpl(SectorTypeRepository):
    """Implementación del repositorio para tipos de sector"""
    
    async def create(self, sector_type: SectorType) -> SectorType:
        """Crear un nuevo tipo de sector"""
        async for session in get_db_session():
            # Verificar si ya existe un tipo con el mismo nombre o código
            if await self.exists_by_name_or_code(sector_type.name, sector_type.code):
                raise SectorTypeAlreadyExistsException(
                    f"Ya existe un tipo de sector con el nombre '{sector_type.name}' o código '{sector_type.code}'",
                    name=sector_type.name,
                    code=sector_type.code
                )
            
            # Crear el modelo
            sector_type_model = SectorTypeModel(
                name=sector_type.name,
                code=sector_type.code,
                description=sector_type.description,
                measurement_unit=sector_type.measurement_unit,
                is_active=sector_type.is_active
            )
            
            session.add(sector_type_model)
            await session.commit()
            await session.refresh(sector_type_model)
            
            # Retornar entidad del dominio
            return SectorType(
                id=sector_type_model.id,
                name=sector_type_model.name,
                code=sector_type_model.code,
                description=sector_type_model.description,
                measurement_unit=sector_type_model.measurement_unit,
                is_active=sector_type_model.is_active,
                created_at=sector_type_model.created_at,
                updated_at=sector_type_model.updated_at
            )
    
    async def get_by_id(self, sector_type_id: int) -> Optional[SectorType]:
        """Obtener un tipo de sector por ID"""
        async for session in get_db_session():
            result = await session.execute(
                select(SectorTypeModel).where(SectorTypeModel.id == sector_type_id)
            )
            sector_type_model = result.scalar_one_or_none()
            
            if not sector_type_model:
                return None
            
            return SectorType(
                id=sector_type_model.id,
                name=sector_type_model.name,
                code=sector_type_model.code,
                description=sector_type_model.description,
                measurement_unit=sector_type_model.measurement_unit,
                is_active=sector_type_model.is_active,
                created_at=sector_type_model.created_at,
                updated_at=sector_type_model.updated_at
            )
    
    async def get_by_code(self, code: str) -> Optional[SectorType]:
        """Obtener un tipo de sector por código"""
        async for session in get_db_session():
            result = await session.execute(
                select(SectorTypeModel).where(SectorTypeModel.code == code)
            )
            sector_type_model = result.scalar_one_or_none()
            
            if not sector_type_model:
                return None
            
            return SectorType(
                id=sector_type_model.id,
                name=sector_type_model.name,
                code=sector_type_model.code,
                description=sector_type_model.description,
                measurement_unit=sector_type_model.measurement_unit,
                is_active=sector_type_model.is_active,
                created_at=sector_type_model.created_at,
                updated_at=sector_type_model.updated_at
            )
    
    async def list(self, filter_request: SectorTypeFilterRequest) -> Tuple[List[SectorType], int]:
        """Listar tipos de sector con filtros y paginación"""
        async for session in get_db_session():
            query = select(SectorTypeModel)
            
            # Aplicar filtros
            if filter_request.name:
                query = query.where(SectorTypeModel.name.ilike(f"%{filter_request.name}%"))
            
            if filter_request.code:
                query = query.where(SectorTypeModel.code.ilike(f"%{filter_request.code}%"))
            
            if filter_request.is_active is not None:
                query = query.where(SectorTypeModel.is_active == filter_request.is_active)
            
            # Contar total
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await session.execute(count_query)
            total = total_result.scalar()
            
            # Aplicar paginación y ordenamiento
            query = query.offset(filter_request.offset).limit(filter_request.limit).order_by(SectorTypeModel.name)
            
            result = await session.execute(query)
            sector_type_models = result.scalars().all()
            
            # Convertir a entidades del dominio
            sector_types = [
                SectorType(
                    id=model.id,
                    name=model.name,
                    code=model.code,
                    description=model.description,
                    measurement_unit=model.measurement_unit,
                    is_active=model.is_active,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in sector_type_models
            ]
            
            return sector_types, total
    
    async def update(self, sector_type: SectorType) -> SectorType:
        """Actualizar un tipo de sector"""
        async for session in get_db_session():
            result = await session.execute(
                select(SectorTypeModel).where(SectorTypeModel.id == sector_type.id)
            )
            sector_type_model = result.scalar_one_or_none()
            
            if not sector_type_model:
                raise SectorTypeNotFoundException(f"Tipo de sector con ID {sector_type.id} no encontrado")
            
            # Verificar si ya existe otro tipo con el mismo nombre o código
            if await self.exists_by_name_or_code(sector_type.name, sector_type.code, exclude_id=sector_type.id):
                raise SectorTypeAlreadyExistsException(
                    f"Ya existe un tipo de sector con el nombre '{sector_type.name}' o código '{sector_type.code}'",
                    name=sector_type.name,
                    code=sector_type.code
                )
            
            # Actualizar campos
            sector_type_model.name = sector_type.name
            sector_type_model.code = sector_type.code
            sector_type_model.description = sector_type.description
            sector_type_model.measurement_unit = sector_type.measurement_unit
            sector_type_model.is_active = sector_type.is_active
            
            await session.commit()
            await session.refresh(sector_type_model)
            
            return SectorType(
                id=sector_type_model.id,
                name=sector_type_model.name,
                code=sector_type_model.code,
                description=sector_type_model.description,
                measurement_unit=sector_type_model.measurement_unit,
                is_active=sector_type_model.is_active,
                created_at=sector_type_model.created_at,
                updated_at=sector_type_model.updated_at
            )
    
    async def delete(self, sector_type_id: int) -> bool:
        """Eliminar un tipo de sector"""
        async for session in get_db_session():
            result = await session.execute(
                select(SectorTypeModel).where(SectorTypeModel.id == sector_type_id)
            )
            sector_type_model = result.scalar_one_or_none()
            
            if not sector_type_model:
                return False
            
            await session.delete(sector_type_model)
            await session.commit()
            
            return True
    
    async def exists_by_name_or_code(self, name: str, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un tipo de sector con el nombre o código dado"""
        async for session in get_db_session():
            query = select(SectorTypeModel).where(
                (SectorTypeModel.name == name) | (SectorTypeModel.code == code)
            )
            
            if exclude_id:
                query = query.where(SectorTypeModel.id != exclude_id)
            
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None 