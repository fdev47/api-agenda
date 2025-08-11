"""
Interfaz del repositorio de Customer
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ...domain.entities.customer import Customer


class CustomerRepository(ABC):
    """Interfaz del repositorio de Customer"""

    @abstractmethod
    async def create(self, customer: Customer) -> Customer:
        """Crear un nuevo customer"""
        pass

    @abstractmethod
    async def get_by_id(self, customer_id: UUID) -> Optional[Customer]:
        """Obtener un customer por ID"""
        pass

    @abstractmethod
    async def get_by_auth_uid(self, auth_uid: str) -> Optional[Customer]:
        """Obtener un customer por auth_uid"""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[Customer]:
        """Obtener un customer por username"""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Obtener todos los customers"""
        pass

    @abstractmethod
    async def update(self, customer_id: UUID, update_data: dict) -> Optional[Customer]:
        """Actualizar un customer"""
        pass

    @abstractmethod
    async def delete(self, customer_id: UUID) -> bool:
        """Eliminar un customer"""
        pass 