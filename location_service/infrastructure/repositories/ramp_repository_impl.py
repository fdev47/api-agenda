"""
Implementación del repositorio para rampas
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, or_, select, func
from ...domain.interfaces.ramp_repository import RampRepository
from ...domain.entities.ramp import Ramp
from ...domain.dto.requests.ramp_requests import RampFilterRequest
from ..models.ramp import Ramp as RampModel


class RampRepositoryImpl(RampRepository):
    """Implementación del repositorio para rampas"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, ramp: Ramp) -> Ramp:
        """Crear una nueva rampa"""
        ramp_model = RampModel(
            name=ramp.name,
            is_available=ramp.is_available,
            branch_id=ramp.branch_id
        )
        
        self.session.add(ramp_model)
        await self.session.commit()
        await self.session.refresh(ramp_model)
        
        return Ramp(
            id=ramp_model.id,
            name=ramp_model.name,
            is_available=ramp_model.is_available,
            branch_id=ramp_model.branch_id,
            created_at=ramp_model.created_at,
            updated_at=ramp_model.updated_at
        )
    
    async def get_by_id(self, ramp_id: int) -> Optional[Ramp]:
        """Obtener una rampa por ID"""
        result = await self.session.execute(
            select(RampModel).where(RampModel.id == ramp_id)
        )
        ramp_model = result.scalar_one_or_none()
        
        if not ramp_model:
            return None
        
        return Ramp(
            id=ramp_model.id,
            name=ramp_model.name,
            is_available=ramp_model.is_available,
            branch_id=ramp_model.branch_id,
            created_at=ramp_model.created_at,
            updated_at=ramp_model.updated_at
        )
    
    async def get_by_branch_id(self, branch_id: int) -> List[Ramp]:
        """Obtener todas las rampas de una sucursal"""
        result = await self.session.execute(
            select(RampModel)
            .where(RampModel.branch_id == branch_id)
            .order_by(RampModel.name)
        )
        ramp_models = result.scalars().all()
        
        return [
            Ramp(
                id=ramp_model.id,
                name=ramp_model.name,
                is_available=ramp_model.is_available,
                branch_id=ramp_model.branch_id,
                created_at=ramp_model.created_at,
                updated_at=ramp_model.updated_at
            )
            for ramp_model in ramp_models
        ]
    
    async def list(self, filter_request: RampFilterRequest) -> tuple[List[Ramp], int]:
        """Listar rampas con filtros y paginación"""
        query = select(RampModel)
        
        # Aplicar filtros
        if filter_request.name:
            query = query.where(RampModel.name.ilike(f"%{filter_request.name}%"))
        
        if filter_request.branch_id:
            query = query.where(RampModel.branch_id == filter_request.branch_id)
        
        if filter_request.is_available is not None:
            query = query.where(RampModel.is_available == filter_request.is_available)
        
        # Contar total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Aplicar paginación y ordenamiento
        query = query.offset(filter_request.offset).limit(filter_request.limit).order_by(RampModel.name)
        
        result = await self.session.execute(query)
        ramp_models = result.scalars().all()
        
        ramps = [
            Ramp(
                id=ramp_model.id,
                name=ramp_model.name,
                is_available=ramp_model.is_available,
                branch_id=ramp_model.branch_id,
                created_at=ramp_model.created_at,
                updated_at=ramp_model.updated_at
            )
            for ramp_model in ramp_models
        ]
        
        return ramps, total
    
    async def update(self, ramp: Ramp) -> Ramp:
        """Actualizar una rampa"""
        result = await self.session.execute(
            select(RampModel).where(RampModel.id == ramp.id)
        )
        ramp_model = result.scalar_one_or_none()
        
        if not ramp_model:
            raise ValueError(f"Rampa con ID {ramp.id} no encontrada")
        
        # Actualizar campos
        ramp_model.name = ramp.name
        ramp_model.is_available = ramp.is_available
        ramp_model.branch_id = ramp.branch_id
        
        await self.session.commit()
        await self.session.refresh(ramp_model)
        
        return Ramp(
            id=ramp_model.id,
            name=ramp_model.name,
            is_available=ramp_model.is_available,
            branch_id=ramp_model.branch_id,
            created_at=ramp_model.created_at,
            updated_at=ramp_model.updated_at
        )
    
    async def delete(self, ramp_id: int) -> bool:
        """Eliminar una rampa"""
        result = await self.session.execute(
            select(RampModel).where(RampModel.id == ramp_id)
        )
        ramp_model = result.scalar_one_or_none()
        
        if not ramp_model:
            return False
        
        await self.session.delete(ramp_model)
        await self.session.commit()
        
        return True
    
    async def exists_by_name_and_branch(self, name: str, branch_id: int, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe una rampa con el nombre y sucursal dados"""
        query = select(RampModel).where(
            and_(RampModel.name == name, RampModel.branch_id == branch_id)
        )
        
        if exclude_id:
            query = query.where(RampModel.id != exclude_id)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None 