"""
Interfaz del repositorio de Address
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ...domain.entities.address import Address


class AddressRepository(ABC):
    """Interfaz del repositorio de Address"""
    
    @abstractmethod
    async def create(self, address: Address) -> Address:
        """Crear una nueva dirección"""
        pass
    
    @abstractmethod
    async def get_by_id(self, address_id: UUID) -> Optional[Address]:
        """Obtener una dirección por ID"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Address]:
        """Obtener todas las direcciones"""
        pass
    
    @abstractmethod
    async def update(self, address_id: UUID, address: Address) -> Optional[Address]:
        """Actualizar una dirección"""
        pass
    
    @abstractmethod
    async def delete(self, address_id: UUID) -> bool:
        """Eliminar una dirección"""
        pass 