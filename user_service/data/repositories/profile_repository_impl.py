"""
Implementación del repositorio de perfiles
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from ...domain.interfaces.profile_repository import IProfileRepository
from ...domain.entities.profile import Profile
from ...infrastructure.models.profile import ProfileDB
from ...infrastructure.models.role import RoleDB


class ProfileRepositoryImpl(IProfileRepository):
    """Implementación del repositorio de perfiles"""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def get_by_id(self, profile_id: UUID) -> Optional[Profile]:
        """Obtener perfil por ID"""
        query = select(ProfileDB).options(selectinload(ProfileDB.roles)).where(ProfileDB.id == profile_id)
        result = await self._session.execute(query)
        profile_db = result.scalar_one_or_none()
        
        if profile_db:
            return Profile.model_validate(profile_db)
        return None
    
    async def get_by_name(self, name: str) -> Optional[Profile]:
        """Obtener perfil por nombre"""
        query = select(ProfileDB).options(selectinload(ProfileDB.roles)).where(ProfileDB.name == name)
        result = await self._session.execute(query)
        profile_db = result.scalar_one_or_none()
        
        if profile_db:
            return Profile.model_validate(profile_db)
        return None
    
    async def create(self, profile: Profile) -> Profile:
        """Crear perfil"""
        # Crear el perfil sin roles primero
        profile_db = ProfileDB(
            name=profile.name,
            description=profile.description
        )
        
        self._session.add(profile_db)
        await self._session.commit()
        await self._session.refresh(profile_db)
        
        created_profile = Profile(
            id=profile_db.id,
            name=profile_db.name,
            description=profile_db.description,
            roles=[]
        )
        
        return created_profile
    
    async def assign_roles(self, profile_id: UUID, role_ids: List[UUID]) -> Profile:
        """Asignar roles a un perfil existente"""
        # Obtener el perfil con roles cargados
        query = select(ProfileDB).options(selectinload(ProfileDB.roles)).where(ProfileDB.id == profile_id)
        result = await self._session.execute(query)
        profile_db = result.scalar_one_or_none()
        
        if not profile_db:
            raise ValueError(f"Perfil con ID {profile_id} no encontrado")
        
        # Limpiar roles existentes
        profile_db.roles.clear()
        
        # Asignar nuevos roles
        for role_id in role_ids:
            role_query = select(RoleDB).where(RoleDB.id == role_id)
            role_result = await self._session.execute(role_query)
            role_db = role_result.scalar_one_or_none()
            if role_db:
                profile_db.roles.append(role_db)
        
        await self._session.commit()
        await self._session.refresh(profile_db)
        
        return Profile.model_validate(profile_db)
    
    async def update(self, profile: Profile) -> Profile:
        """Actualizar perfil"""
        query = select(ProfileDB).options(selectinload(ProfileDB.roles)).where(ProfileDB.id == profile.id)
        result = await self._session.execute(query)
        profile_db = result.scalar_one_or_none()
        
        if not profile_db:
            raise ValueError(f"Perfil con ID {profile.id} no encontrado")
        
        profile_db.name = profile.name
        profile_db.description = profile.description
        
        await self._session.commit()
        await self._session.refresh(profile_db)
        
        return Profile.model_validate(profile_db)
    
    async def delete(self, profile_id: UUID) -> bool:
        """Eliminar perfil"""
        query = delete(ProfileDB).where(ProfileDB.id == profile_id)
        result = await self._session.execute(query)
        await self._session.commit()
        
        return result.rowcount > 0
    
    async def list_all(self) -> List[Profile]:
        """Listar todos los perfiles"""
        query = select(ProfileDB).options(selectinload(ProfileDB.roles))
        result = await self._session.execute(query)
        profiles_db = result.scalars().all()
        
        return [Profile.model_validate(profile_db) for profile_db in profiles_db] 