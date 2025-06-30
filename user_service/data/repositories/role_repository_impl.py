"""
Implementación del repositorio de roles
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from ...domain.interfaces.role_repository import IRoleRepository
from ...domain.entities.role import Role
from ...infrastructure.models.role import RoleDB


class RoleRepositoryImpl(IRoleRepository):
    """Implementación del repositorio de roles"""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def get_by_id(self, role_id: UUID) -> Optional[Role]:
        """Obtener rol por ID"""
        query = select(RoleDB).options(selectinload(RoleDB.profiles)).where(RoleDB.id == role_id)
        result = await self._session.execute(query)
        role_db = result.scalar_one_or_none()
        
        if role_db:
            return Role.model_validate(role_db)
        return None
    
    async def get_by_name(self, name: str) -> Optional[Role]:
        """Obtener rol por nombre"""
        query = select(RoleDB).options(selectinload(RoleDB.profiles)).where(RoleDB.name == name)
        result = await self._session.execute(query)
        role_db = result.scalar_one_or_none()
        
        if role_db:
            return Role.model_validate(role_db)
        return None
    
    async def create(self, role: Role) -> Role:
        """Crear rol"""
        role_db = RoleDB(
            name=role.name,
            description=role.description
        )
        
        self._session.add(role_db)
        await self._session.commit()
        await self._session.refresh(role_db)
        
        return Role.model_validate(role_db)
    
    async def update(self, role: Role) -> Role:
        """Actualizar rol"""
        query = select(RoleDB).where(RoleDB.id == role.id)
        result = await self._session.execute(query)
        role_db = result.scalar_one_or_none()
        
        if not role_db:
            raise ValueError(f"Rol con ID {role.id} no encontrado")
        
        # Actualizar campos
        role_db.name = role.name
        role_db.description = role.description
        
        await self._session.commit()
        await self._session.refresh(role_db)
        
        return Role.model_validate(role_db)
    
    async def delete(self, role_id: UUID) -> bool:
        """Eliminar rol"""
        query = delete(RoleDB).where(RoleDB.id == role_id)
        result = await self._session.execute(query)
        await self._session.commit()
        
        return result.rowcount > 0
    
    async def list_all(self) -> List[Role]:
        """Listar todos los roles"""
        query = select(RoleDB).options(selectinload(RoleDB.profiles))
        result = await self._session.execute(query)
        roles_db = result.scalars().all()
        
        return [Role.model_validate(role_db) for role_db in roles_db] 