from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ..entities.user import User
from ..dto.requests.user_requests import CreateUserRequest, UpdateUserRequest

class UserRepository(ABC):
    """Interfaz del repositorio de usuarios"""
    
    @abstractmethod
    async def create(self, user_data: CreateUserRequest) -> User:
        """Crear un nuevo usuario"""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        """Obtener usuario por ID"""
        pass
    
    @abstractmethod
    async def get_by_auth_uid(self, auth_uid: str) -> User | None:
        """Obtener usuario por auth_uid"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Obtener usuario por email"""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        """Obtener usuario por username"""
        pass
    
    @abstractmethod
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Listar usuarios con paginación"""
        pass
    
    @abstractmethod
    async def update(self, user_id: UUID, user_data: UpdateUserRequest) -> User | None:
        """Actualizar usuario"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Eliminar usuario"""
        pass
    
    @abstractmethod
    async def activate(self, user_id: UUID) -> User | None:
        """Activar usuario"""
        pass
    
    @abstractmethod
    async def deactivate(self, user_id: UUID) -> User | None:
        """Desactivar usuario"""
        pass
