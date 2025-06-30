"""
Implementación del repositorio para sectores
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ...domain.interfaces.sector_repository import SectorRepository
from ...domain.entities.sector import Sector
from ...domain.dto.requests.sector_requests import SectorFilterRequest
from ...domain.exceptions import SectorNotFoundException, SectorAlreadyExistsException
from ..models.sector import Sector as SectorModel


class SectorRepositoryImpl(SectorRepository):
    """Implementación del repositorio para sectores"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, sector: Sector) -> Sector:
        """Crear un nuevo sector"""
        # Verificar si ya existe un sector con el mismo nombre en la misma sucursal
        if await self.exists_by_name_and_branch(sector.name, sector.branch_id):
            raise SectorAlreadyExistsException(
                f"Ya existe un sector con el nombre '{sector.name}' en la sucursal {sector.branch_id}",
                name=sector.name,
                branch_id=sector.branch_id
            )
        
        # Crear el modelo
        sector_model = SectorModel(
            name=sector.name,
            description=sector.description,
            branch_id=sector.branch_id,
            sector_type_id=sector.sector_type_id,
            measurement_unit=sector.measurement_unit
        )
        
        self.session.add(sector_model)
        await self.session.commit()
        await self.session.refresh(sector_model)
        
        # Retornar entidad del dominio
        return Sector(
            id=sector_model.id,
            name=sector_model.name,
            description=sector_model.description,
            branch_id=sector_model.branch_id,
            sector_type_id=sector_model.sector_type_id,
            measurement_unit=sector_model.measurement_unit,
            created_at=sector_model.created_at,
            updated_at=sector_model.updated_at
        )
    
    async def get_by_id(self, sector_id: int) -> Optional[Sector]:
        """Obtener un sector por ID"""
        result = await self.session.execute(
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
            measurement_unit=sector_model.measurement_unit,
            created_at=sector_model.created_at,
            updated_at=sector_model.updated_at
        )
    
    async def get_by_branch_id(self, branch_id: int) -> List[Sector]:
        """Obtener todos los sectores de una sucursal"""
        result = await self.session.execute(
            select(SectorModel).where(SectorModel.branch_id == branch_id)
        )
        sector_models = result.scalars().all()
        
        return [
            Sector(
                id=model.id,
                name=model.name,
                description=model.description,
                branch_id=model.branch_id,
                sector_type_id=model.sector_type_id,
                measurement_unit=model.measurement_unit,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in sector_models
        ]
    
    async def list(self, filter_request: SectorFilterRequest) -> Tuple[List[Sector], int]:
        """Listar sectores con filtros y paginación"""
        query = select(SectorModel)
        
        # Aplicar filtros
        if filter_request.name:
            query = query.where(SectorModel.name.ilike(f"%{filter_request.name}%"))
        
        if filter_request.branch_id:
            query = query.where(SectorModel.branch_id == filter_request.branch_id)
        
        if filter_request.sector_type_id:
            query = query.where(SectorModel.sector_type_id == filter_request.sector_type_id)
        
        if filter_request.measurement_unit:
            query = query.where(SectorModel.measurement_unit == filter_request.measurement_unit)
        
        # Contar total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Aplicar paginación
        query = query.offset(filter_request.offset).limit(filter_request.limit)
        
        # Ejecutar consulta
        result = await self.session.execute(query)
        sector_models = result.scalars().all()
        
        # Convertir a entidades del dominio
        sectors = [
            Sector(
                id=model.id,
                name=model.name,
                description=model.description,
                branch_id=model.branch_id,
                sector_type_id=model.sector_type_id,
                measurement_unit=model.measurement_unit,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in sector_models
        ]
        
        return sectors, total
    
    async def update(self, sector: Sector) -> Sector:
        """Actualizar un sector"""
        # Verificar si existe
        existing_model = await self.session.get(SectorModel, sector.id)
        if not existing_model:
            raise SectorNotFoundException(
                f"No se encontró el sector con ID {sector.id}",
                entity_id=sector.id
            )
        
        # Verificar si ya existe otro sector con el mismo nombre en la misma sucursal
        if await self.exists_by_name_and_branch(sector.name, sector.branch_id, exclude_id=sector.id):
            raise SectorAlreadyExistsException(
                f"Ya existe un sector con el nombre '{sector.name}' en la sucursal {sector.branch_id}",
                name=sector.name,
                branch_id=sector.branch_id
            )
        
        # Actualizar campos
        existing_model.name = sector.name
        existing_model.description = sector.description
        existing_model.sector_type_id = sector.sector_type_id
        existing_model.measurement_unit = sector.measurement_unit
        
        await self.session.commit()
        await self.session.refresh(existing_model)
        
        return Sector(
            id=existing_model.id,
            name=existing_model.name,
            description=existing_model.description,
            branch_id=existing_model.branch_id,
            sector_type_id=existing_model.sector_type_id,
            measurement_unit=existing_model.measurement_unit,
            created_at=existing_model.created_at,
            updated_at=existing_model.updated_at
        )
    
    async def delete(self, sector_id: int) -> bool:
        """Eliminar un sector"""
        sector_model = await self.session.get(SectorModel, sector_id)
        if not sector_model:
            raise SectorNotFoundException(
                f"No se encontró el sector con ID {sector_id}",
                entity_id=sector_id
            )
        
        await self.session.delete(sector_model)
        await self.session.commit()
        
        return True
    
    async def exists_by_name_and_branch(self, name: str, branch_id: int, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un sector con el mismo nombre en la misma sucursal"""
        query = select(SectorModel).where(
            (SectorModel.name == name) & (SectorModel.branch_id == branch_id)
        )
        
        if exclude_id:
            query = query.where(SectorModel.id != exclude_id)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None 