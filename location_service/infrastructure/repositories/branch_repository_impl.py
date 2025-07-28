"""
Implementación del repositorio para sucursales
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, or_, select, func
from ...domain.interfaces.branch_repository import BranchRepository
from ...domain.entities.branch import Branch
from ...domain.dto.requests.branch_requests import BranchFilterRequest
from ..models.branch import Branch as BranchModel


class BranchRepositoryImpl(BranchRepository):
    """Implementación del repositorio para sucursales"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, branch: Branch) -> Branch:
        """Crear una nueva sucursal"""
        branch_model = BranchModel(
            name=branch.name,
            code=branch.code,
            local_id=branch.local_id,
            country_id=branch.country_id,
            state_id=branch.state_id,
            city_id=branch.city_id,
            address=branch.address,
            is_active=branch.is_active
        )
        
        self.session.add(branch_model)
        await self.session.commit()
        await self.session.refresh(branch_model)
        
        return Branch(
            id=branch_model.id,
            name=branch_model.name,
            code=branch_model.code,
            local_id=branch_model.local_id,
            country_id=branch_model.country_id,
            state_id=branch_model.state_id,
            city_id=branch_model.city_id,
            address=branch_model.address,
            ramps=0,  # Valor por defecto
            is_active=branch_model.is_active,
            created_at=branch_model.created_at,
            updated_at=branch_model.updated_at
        )
    
    async def get_by_id(self, branch_id: int) -> Optional[Branch]:
        """Obtener una sucursal por ID"""
        result = await self.session.execute(
            select(BranchModel).where(BranchModel.id == branch_id)
        )
        branch_model = result.scalar_one_or_none()
        
        if not branch_model:
            return None
        
        return Branch(
            id=branch_model.id,
            name=branch_model.name,
            code=branch_model.code,
            local_id=branch_model.local_id,
            country_id=branch_model.country_id,
            state_id=branch_model.state_id,
            city_id=branch_model.city_id,
            address=branch_model.address,
            ramps=0,  # Valor por defecto
            is_active=branch_model.is_active,
            created_at=branch_model.created_at,
            updated_at=branch_model.updated_at
        )
    
    async def get_by_code(self, code: str) -> Optional[Branch]:
        """Obtener una sucursal por código"""
        result = await self.session.execute(
            select(BranchModel).where(BranchModel.code == code)
        )
        branch_model = result.scalar_one_or_none()
        
        if not branch_model:
            return None
        
        return Branch(
            id=branch_model.id,
            name=branch_model.name,
            code=branch_model.code,
            local_id=branch_model.local_id,
            country_id=branch_model.country_id,
            state_id=branch_model.state_id,
            city_id=branch_model.city_id,
            address=branch_model.address,
            ramps=0,  # Valor por defecto
            is_active=branch_model.is_active,
            created_at=branch_model.created_at,
            updated_at=branch_model.updated_at
        )
    
    async def list_all(self, filter_request: BranchFilterRequest) -> Tuple[List[Branch], int]:
        """Listar todas las sucursales con filtros"""
        query = select(BranchModel)
        
        # Aplicar filtros
        if filter_request.name:
            query = query.where(BranchModel.name.ilike(f"%{filter_request.name}%"))
        
        if filter_request.code:
            query = query.where(BranchModel.code.ilike(f"%{filter_request.code}%"))
        
        if filter_request.local_id:
            query = query.where(BranchModel.local_id == filter_request.local_id)
        
        if filter_request.country_id:
            query = query.where(BranchModel.country_id == filter_request.country_id)
        
        if filter_request.state_id:
            query = query.where(BranchModel.state_id == filter_request.state_id)
        
        if filter_request.city_id:
            query = query.where(BranchModel.city_id == filter_request.city_id)
        
        if filter_request.is_active is not None:
            query = query.where(BranchModel.is_active == filter_request.is_active)
        
        # Contar total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Aplicar paginación y ordenamiento
        query = query.offset(filter_request.offset).limit(filter_request.limit).order_by(BranchModel.name)
        
        result = await self.session.execute(query)
        branch_models = result.scalars().all()
        
        branches = [
            Branch(
                id=branch_model.id,
                name=branch_model.name,
                code=branch_model.code,
                local_id=branch_model.local_id,
                country_id=branch_model.country_id,
                state_id=branch_model.state_id,
                city_id=branch_model.city_id,
                address=branch_model.address,
                ramps=0,  # Valor por defecto
                is_active=branch_model.is_active,
                created_at=branch_model.created_at,
                updated_at=branch_model.updated_at
            )
            for branch_model in branch_models
        ]
        
        return branches, total
    
    async def list_by_local(self, local_id: int) -> List[Branch]:
        """Listar sucursales por local"""
        result = await self.session.execute(
            select(BranchModel)
            .where(BranchModel.local_id == local_id)
            .order_by(BranchModel.name)
        )
        branch_models = result.scalars().all()
        
        return [
            Branch(
                id=branch_model.id,
                name=branch_model.name,
                code=branch_model.code,
                local_id=branch_model.local_id,
                country_id=branch_model.country_id,
                state_id=branch_model.state_id,
                city_id=branch_model.city_id,
                address=branch_model.address,
                ramps=0,  # Valor por defecto
                is_active=branch_model.is_active,
                created_at=branch_model.created_at,
                updated_at=branch_model.updated_at
            )
            for branch_model in branch_models
        ]
    
    async def update(self, branch_id: int, branch: Branch) -> Optional[Branch]:
        """Actualizar una sucursal"""
        result = await self.session.execute(
            select(BranchModel).where(BranchModel.id == branch_id)
        )
        branch_model = result.scalar_one_or_none()
        
        if not branch_model:
            return None
        
        # Actualizar campos
        if branch.name is not None:
            branch_model.name = branch.name
        if branch.code is not None:
            branch_model.code = branch.code
        if branch.local_id is not None:
            branch_model.local_id = branch.local_id
        if branch.country_id is not None:
            branch_model.country_id = branch.country_id
        if branch.state_id is not None:
            branch_model.state_id = branch.state_id
        if branch.city_id is not None:
            branch_model.city_id = branch.city_id
        if branch.address is not None:
            branch_model.address = branch.address
        if branch.is_active is not None:
            branch_model.is_active = branch.is_active
        
        await self.session.commit()
        await self.session.refresh(branch_model)
        
        return Branch(
            id=branch_model.id,
            name=branch_model.name,
            code=branch_model.code,
            local_id=branch_model.local_id,
            country_id=branch_model.country_id,
            state_id=branch_model.state_id,
            city_id=branch_model.city_id,
            address=branch_model.address,
            ramps=0,  # Valor por defecto
            is_active=branch_model.is_active,
            created_at=branch_model.created_at,
            updated_at=branch_model.updated_at
        )
    
    async def delete(self, branch_id: int) -> bool:
        """Eliminar una sucursal"""
        result = await self.session.execute(
            select(BranchModel).where(BranchModel.id == branch_id)
        )
        branch_model = result.scalar_one_or_none()
        
        if not branch_model:
            return False
        
        await self.session.delete(branch_model)
        await self.session.commit()
        
        return True
    
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe una sucursal con el código dado"""
        query = select(BranchModel).where(BranchModel.code == code)
        
        if exclude_id:
            query = query.where(BranchModel.id != exclude_id)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
    
    async def exists_by_id(self, branch_id: int) -> bool:
        """Verificar si existe una sucursal con el ID dado"""
        result = await self.session.execute(
            select(BranchModel).where(BranchModel.id == branch_id)
        )
        return result.scalar_one_or_none() is not None
    
    async def exists_by_local_id(self, local_id: int) -> bool:
        """Verificar si existe un local con el ID dado"""
        from ..models.local import Local as LocalModel
        result = await self.session.execute(
            select(LocalModel).where(LocalModel.id == local_id)
        )
        return result.scalar_one_or_none() is not None 