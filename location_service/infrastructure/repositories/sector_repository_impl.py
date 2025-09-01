"""
Implementación del repositorio para sectores
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ...domain.interfaces.sector_repository import SectorRepository
from ...domain.entities.sector import Sector
from ...domain.dto.requests.sector_requests import SectorFilterRequest
from ..models.sector import Sector as SectorModel
from commons.database import get_db_session
from ...domain.entities.measurement_unit import MeasurementUnit


class SectorRepositoryImpl(SectorRepository):
    """Implementación del repositorio para sectores"""
    
    async def create(self, sector: Sector) -> Sector:
        """Crear un nuevo sector"""
        async for session in get_db_session():
            # Crear el modelo
            sector_model = SectorModel(
                name=sector.name,
                description=sector.description,
                branch_id=sector.branch_id,
                sector_type_id=sector.sector_type_id,
                is_active=sector.is_active
            )
            
            session.add(sector_model)
            await session.commit()
            await session.refresh(sector_model)
            
            # Retornar entidad del dominio
            return Sector(
                id=sector_model.id,
                name=sector_model.name,
                description=sector_model.description,
                branch_id=sector_model.branch_id,
                sector_type_id=sector_model.sector_type_id,
                is_active=sector_model.is_active,
                created_at=sector_model.created_at,
                updated_at=sector_model.updated_at
            )
    
    async def get_by_id(self, sector_id: int) -> Optional[Sector]:
        """Obtener un sector por ID"""
        async for session in get_db_session():
            result = await session.execute(
                select(SectorModel).where(SectorModel.id == sector_id)
            )
            sector_model = result.scalar_one_or_none()
            
            if not sector_model:
                return None
            
            return Sector(
                id=sector_model.id,
                name=sector_model.name,
                description=sector_model.description,
                branch_id=sector_model.branch_id,
                sector_type_id=sector_model.sector_type_id,
                is_active=sector_model.is_active,
                created_at=sector_model.created_at,
                updated_at=sector_model.updated_at
            )
    
    async def get_by_code(self, code: str) -> Optional[Sector]:
        """Obtener un sector por código"""
        async for session in get_db_session():
            result = await session.execute(
                select(SectorModel).where(SectorModel.code == code)
            )
            sector_model = result.scalar_one_or_none()
            
            if not sector_model:
                return None
            
            return Sector(
                id=sector_model.id,
                name=sector_model.name,
                code=sector_model.code,
                description=sector_model.description,
                sector_type_id=sector_model.sector_type_id,
                is_active=sector_model.is_active,
                created_at=sector_model.created_at,
                updated_at=sector_model.updated_at
            )
    
    async def list(self, filter_request: SectorFilterRequest) -> Tuple[List[Sector], int]:
        """Listar sectores con filtros y paginación"""
        async for session in get_db_session():
            query = select(SectorModel)
            
            # Aplicar filtros
            if filter_request.name:
                query = query.where(SectorModel.name.ilike(f"%{filter_request.name}%"))
            
            if filter_request.branch_id:
                query = query.where(SectorModel.branch_id == filter_request.branch_id)
            
            if filter_request.sector_type_id:
                query = query.where(SectorModel.sector_type_id == filter_request.sector_type_id)
            
            if filter_request.is_active is not None:
                query = query.where(SectorModel.is_active == filter_request.is_active)
            
            # Contar total
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await session.execute(count_query)
            total = total_result.scalar()
            
            # Aplicar paginación y ordenamiento
            query = query.offset(filter_request.offset).limit(filter_request.limit).order_by(SectorModel.name)
            
            result = await session.execute(query)
            sector_models = result.scalars().all()
            
            # Convertir a entidades del dominio
            sectors = [
                Sector(
                    id=model.id,
                    name=model.name,
                    description=model.description,
                    branch_id=model.branch_id,
                    sector_type_id=model.sector_type_id,
                    is_active=model.is_active,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in sector_models
            ]
            
            return sectors, total
    
    async def get_by_branch_id(self, branch_id: int) -> List[Sector]:
        """Obtener todos los sectores de una sucursal"""
        async for session in get_db_session():
            result = await session.execute(
                select(SectorModel)
                .where(SectorModel.branch_id == branch_id)
                .order_by(SectorModel.name)
            )
            sector_models = result.scalars().all()
            
            return [
                Sector(
                    id=model.id,
                    name=model.name,
                    description=model.description,
                    branch_id=model.branch_id,
                    sector_type_id=model.sector_type_id,
                    is_active=model.is_active,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in sector_models
            ]
    
    async def update(self, sector: Sector) -> Sector:
        """Actualizar un sector"""
        async for session in get_db_session():
            result = await session.execute(
                select(SectorModel).where(SectorModel.id == sector.id)
            )
            sector_model = result.scalar_one_or_none()
            
            if not sector_model:
                raise ValueError(f"Sector con ID {sector.id} no encontrado")
            
            # Actualizar campos
            sector_model.name = sector.name
            sector_model.description = sector.description
            sector_model.branch_id = sector.branch_id
            sector_model.sector_type_id = sector.sector_type_id
            sector_model.is_active = sector.is_active
            
            await session.commit()
            await session.refresh(sector_model)
            
            return Sector(
                id=sector_model.id,
                name=sector_model.name,
                description=sector_model.description,
                branch_id=sector_model.branch_id,
                sector_type_id=sector_model.sector_type_id,
                is_active=sector_model.is_active,
                created_at=sector_model.created_at,
                updated_at=sector_model.updated_at
            )
    
    async def delete(self, sector_id: int) -> bool:
        """Eliminar un sector"""
        async for session in get_db_session():
            result = await session.execute(
                select(SectorModel).where(SectorModel.id == sector_id)
            )
            sector_model = result.scalar_one_or_none()
            
            if not sector_model:
                return False
            
            await session.delete(sector_model)
            await session.commit()
            
            return True
    
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un sector con el código dado"""
        async for session in get_db_session():
            query = select(SectorModel).where(SectorModel.code == code)
            
            if exclude_id:
                query = query.where(SectorModel.id != exclude_id)
            
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None
    
    async def exists_by_id(self, sector_id: int) -> bool:
        """Verificar si existe un sector con el ID dado"""
        async for session in get_db_session():
            result = await session.execute(
                select(SectorModel).where(SectorModel.id == sector_id)
            )
            return result.scalar_one_or_none() is not None 
    
    async def exists_by_name_and_branch(self, name: str, branch_id: int, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un sector con el mismo nombre en la misma sucursal"""
        async for session in get_db_session():
            query = select(SectorModel).where(
                (SectorModel.name == name) & (SectorModel.branch_id == branch_id)
            )
            
            if exclude_id:
                query = query.where(SectorModel.id != exclude_id)
            
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None 