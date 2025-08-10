"""
Implementación del repositorio de usuarios
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from ...domain.interfaces.user_repository import UserRepository
from ...domain.entities.user import User
from ...domain.dto.requests.user_requests import CreateUserRequest, UpdateUserRequest
from ...domain.exceptions.user_exceptions import UserAlreadyExistsException
from ...infrastructure.models.user import UserDB
from ...infrastructure.models.profile import ProfileDB


class UserRepositoryImpl(UserRepository):
    """Implementación del repositorio de usuarios"""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Obtener usuario por ID"""
        query = select(UserDB).options(selectinload(UserDB.profiles)).where(UserDB.id == user_id)
        result = await self._session.execute(query)
        user_db = result.scalar_one_or_none()
        
        if user_db:
            return User.model_validate(user_db)
        return None
    
    async def get_by_auth_uid(self, auth_uid: str) -> Optional[User]:
        """Obtener usuario por auth_uid"""
        query = select(UserDB).options(selectinload(UserDB.profiles)).where(UserDB.auth_uid == auth_uid)
        result = await self._session.execute(query)
        user_db = result.scalar_one_or_none()
        
        if user_db:
            return User.model_validate(user_db)
        return None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        query = select(UserDB).options(selectinload(UserDB.profiles)).where(UserDB.email == email)
        result = await self._session.execute(query)
        user_db = result.scalar_one_or_none()
        
        if user_db:
            return User.model_validate(user_db)
        return None
    
    async def create(self, user_data: CreateUserRequest) -> User:
        """Crear usuario"""
        user_db = UserDB(
            auth_uid=user_data.auth_uid,
            email=user_data.email,
            username=user_data.username,  # Agregar username
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            cellphone_number=user_data.cellphone_number,
            cellphone_country_code=user_data.cellphone_country_code,
            is_active=user_data.is_active,
            user_type=user_data.user_type.value
        )
        
        # Asignar perfiles si se proporcionan
        if user_data.profile_ids:
            for profile_id in user_data.profile_ids:
                profile_query = select(ProfileDB).where(ProfileDB.id == profile_id)
                profile_result = await self._session.execute(profile_query)
                profile_db = profile_result.scalar_one_or_none()
                if profile_db:
                    user_db.profiles.append(profile_db)
        
        self._session.add(user_db)
        try:
            await self._session.commit()
            await self._session.refresh(user_db)
            
            # Recargar el usuario con las relaciones explícitamente
            # Solo cargar perfiles, sin cargar roles
            query = select(UserDB).options(
                selectinload(UserDB.profiles)
            ).where(UserDB.id == user_db.id)
            result = await self._session.execute(query)
            user_db_with_relations = result.scalar_one()
            
        except IntegrityError:
            raise UserAlreadyExistsException(f"User with auth_uid '{user_data.auth_uid}' or email '{user_data.email}' already exists.")
        
        return User.model_validate(user_db_with_relations)
    
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Listar usuarios con paginación"""
        query = select(UserDB).options(selectinload(UserDB.profiles)).offset(skip).limit(limit)
        result = await self._session.execute(query)
        users_db = result.scalars().all()
        
        return [User.model_validate(user_db) for user_db in users_db]
    
    async def update(self, user_id: UUID, user_data: UpdateUserRequest) -> Optional[User]:
        """Actualizar usuario"""
        query = select(UserDB).where(UserDB.id == user_id)
        result = await self._session.execute(query)
        user_db = result.scalar_one_or_none()
        
        if not user_db:
            return None
        
        # Actualizar campos si están presentes
        if user_data.first_name is not None:
            user_db.first_name = user_data.first_name
        if user_data.last_name is not None:
            user_db.last_name = user_data.last_name
        if user_data.phone is not None:
            user_db.phone = user_data.phone
        if user_data.cellphone_number is not None:
            user_db.cellphone_number = user_data.cellphone_number
        if user_data.cellphone_country_code is not None:
            user_db.cellphone_country_code = user_data.cellphone_country_code
        if user_data.is_active is not None:
            user_db.is_active = user_data.is_active
        if user_data.user_type is not None:
            user_db.user_type = user_data.user_type.value
        
        # Actualizar perfiles si se proporcionan
        if user_data.profile_ids is not None:
            # Limpiar perfiles existentes
            user_db.profiles.clear()
            # Asignar nuevos perfiles
            for profile_id in user_data.profile_ids:
                profile_query = select(ProfileDB).where(ProfileDB.id == profile_id)
                profile_result = await self._session.execute(profile_query)
                profile_db = profile_result.scalar_one_or_none()
                if profile_db:
                    user_db.profiles.append(profile_db)
        
        await self._session.commit()
        await self._session.refresh(user_db)
        
        # Recargar el usuario con las relaciones explícitamente
        # Solo cargar perfiles, sin cargar roles
        query = select(UserDB).options(
            selectinload(UserDB.profiles)
        ).where(UserDB.id == user_db.id)
        result = await self._session.execute(query)
        user_db_with_relations = result.scalar_one()
        
        return User.model_validate(user_db_with_relations)
    
    async def delete(self, user_id: UUID) -> bool:
        """Eliminar usuario"""
        query = delete(UserDB).where(UserDB.id == user_id)
        result = await self._session.execute(query)
        await self._session.commit()
        
        return result.rowcount > 0
    
    async def activate(self, user_id: UUID) -> Optional[User]:
        """Activar usuario"""
        query = select(UserDB).where(UserDB.id == user_id)
        result = await self._session.execute(query)
        user_db = result.scalar_one_or_none()
        
        if not user_db:
            return None
        
        user_db.is_active = True
        await self._session.commit()
        await self._session.refresh(user_db)
        
        # Recargar el usuario con las relaciones explícitamente
        query = select(UserDB).options(
            selectinload(UserDB.profiles)
        ).where(UserDB.id == user_db.id)
        result = await self._session.execute(query)
        user_db_with_relations = result.scalar_one()
        
        return User.model_validate(user_db_with_relations)
    
    async def deactivate(self, user_id: UUID) -> Optional[User]:
        """Desactivar usuario"""
        query = select(UserDB).where(UserDB.id == user_id)
        result = await self._session.execute(query)
        user_db = result.scalar_one_or_none()
        
        if not user_db:
            return None
        
        user_db.is_active = False
        await self._session.commit()
        await self._session.refresh(user_db)
        
        # Recargar el usuario con las relaciones explícitamente
        query = select(UserDB).options(
            selectinload(UserDB.profiles)
        ).where(UserDB.id == user_db.id)
        result = await self._session.execute(query)
        user_db_with_relations = result.scalar_one()
        
        return User.model_validate(user_db_with_relations) 