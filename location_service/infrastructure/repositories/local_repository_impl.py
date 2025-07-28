"""
Implementación del repositorio para locales
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, or_, select, func
from ...domain.interfaces.local_repository import LocalRepository
from ...domain.entities.local import Local
from ...domain.dto.requests.local_requests import LocalFilterRequest
from ..models.local import Local as LocalModel
from commons.database import get_db_session


class LocalRepositoryImpl(LocalRepository):
    """Implementación del repositorio para locales"""
    
    async def create(self, local: Local) -> Local:
        """Crear un nuevo local"""
        async for session in get_db_session():
            local_model = LocalModel(
                name=local.name,
                code=local.code,
                description=local.description,
                phone=local.phone,
                email=local.email,
                is_active=local.is_active
            )
            
            session.add(local_model)
            await session.commit()
            await session.refresh(local_model)
            
            return Local(
                id=local_model.id,
                name=local_model.name,
                code=local_model.code,
                description=local_model.description,
                phone=local_model.phone,
                email=local_model.email,
                is_active=local_model.is_active,
                created_at=local_model.created_at,
                updated_at=local_model.updated_at
            )
    
    async def get_by_id(self, local_id: int) -> Optional[Local]:
        """Obtener un local por ID"""
        async for session in get_db_session():
            result = await session.execute(
                select(LocalModel).where(LocalModel.id == local_id)
            )
            local_model = result.scalar_one_or_none()
            
            if not local_model:
                return None
            
            return Local(
                id=local_model.id,
                name=local_model.name,
                code=local_model.code,
                description=local_model.description,
                phone=local_model.phone,
                email=local_model.email,
                is_active=local_model.is_active,
                created_at=local_model.created_at,
                updated_at=local_model.updated_at
            )
    
    async def get_by_code(self, code: str) -> Optional[Local]:
        """Obtener un local por código"""
        async for session in get_db_session():
            result = await session.execute(
                select(LocalModel).where(LocalModel.code == code)
            )
            local_model = result.scalar_one_or_none()
            
            if not local_model:
                return None
            
            return Local(
                id=local_model.id,
                name=local_model.name,
                code=local_model.code,
                description=local_model.description,
                phone=local_model.phone,
                email=local_model.email,
                is_active=local_model.is_active,
                created_at=local_model.created_at,
                updated_at=local_model.updated_at
            )
    
    async def list_all(self, filter_request: LocalFilterRequest) -> Tuple[List[Local], int]:
        """Listar todos los locales con filtros"""
        async for session in get_db_session():
            query = select(LocalModel)
            
            # Aplicar filtros
            if filter_request.name:
                query = query.where(LocalModel.name.ilike(f"%{filter_request.name}%"))
            
            if filter_request.code:
                query = query.where(LocalModel.code.ilike(f"%{filter_request.code}%"))
            
            if filter_request.is_active is not None:
                query = query.where(LocalModel.is_active == filter_request.is_active)
            
            # Contar total
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await session.execute(count_query)
            total = total_result.scalar()
            
            # Aplicar paginación y ordenamiento
            query = query.offset(filter_request.offset).limit(filter_request.limit).order_by(LocalModel.name)
            
            result = await session.execute(query)
            local_models = result.scalars().all()
            
            # Convertir a entidades del dominio
            locals = [
                Local(
                    id=model.id,
                    name=model.name,
                    code=model.code,
                    description=model.description,
                    phone=model.phone,
                    email=model.email,
                    is_active=model.is_active,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in local_models
            ]
            
            return locals, total
    
    async def update(self, local_id: int, local: Local) -> Optional[Local]:
        """Actualizar un local"""
        async for session in get_db_session():
            result = await session.execute(
                select(LocalModel).where(LocalModel.id == local_id)
            )
            local_model = result.scalar_one_or_none()
            
            if not local_model:
                return None
            
            # Actualizar campos
            if local.name is not None:
                local_model.name = local.name
            if local.code is not None:
                local_model.code = local.code
            if local.description is not None:
                local_model.description = local.description
            if local.phone is not None:
                local_model.phone = local.phone
            if local.email is not None:
                local_model.email = local.email
            if local.is_active is not None:
                local_model.is_active = local.is_active
            
            await session.commit()
            await session.refresh(local_model)
            
            return Local(
                id=local_model.id,
                name=local_model.name,
                code=local_model.code,
                description=local_model.description,
                phone=local_model.phone,
                email=local_model.email,
                is_active=local_model.is_active,
                created_at=local_model.created_at,
                updated_at=local_model.updated_at
            )
    
    async def delete(self, local_id: int) -> bool:
        """Eliminar un local"""
        async for session in get_db_session():
            result = await session.execute(
                select(LocalModel).where(LocalModel.id == local_id)
            )
            local_model = result.scalar_one_or_none()
            
            if not local_model:
                return False
            
            await session.delete(local_model)
            await session.commit()
            
            return True
    
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un local con el código dado"""
        async for session in get_db_session():
            query = select(LocalModel).where(LocalModel.code == code)
            
            if exclude_id:
                query = query.where(LocalModel.id != exclude_id)
            
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None
    
    async def exists_by_id(self, local_id: int) -> bool:
        """Verificar si existe un local con el ID dado"""
        async for session in get_db_session():
            result = await session.execute(
                select(LocalModel).where(LocalModel.id == local_id)
            )
            return result.scalar_one_or_none() is not None 