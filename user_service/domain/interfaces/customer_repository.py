"""
Interfaz del repositorio de clientes
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ..entities.customer import Customer
from ..dto.requests.customer_requests import CreateCustomerRequest, UpdateCustomerRequest

class CustomerRepository(ABC):
    """Interfaz del repositorio de clientes"""
    
    @abstractmethod
    async def create(self, customer_data: CreateCustomerRequest) -> Customer:
        """Crear un nuevo cliente"""
        pass
    
    @abstractmethod
    async def get_by_id(self, customer_id: UUID) -> Customer | None:
        """Obtener cliente por ID"""
        pass
    
    @abstractmethod
    async def get_by_auth_uid(self, auth_uid: str) -> Customer | None:
        """Obtener cliente por auth_uid"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Customer | None:
        """Obtener cliente por email"""
        pass
    
    @abstractmethod
    async def get_by_ruc(self, ruc: str) -> Customer | None:
        """Obtener cliente por RUC"""
        pass
    
    @abstractmethod
    async def list_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Listar clientes con paginación"""
        pass
    
    @abstractmethod
    async def update(self, customer_id: UUID, customer_data: UpdateCustomerRequest) -> Customer | None:
        """Actualizar cliente"""
        pass
    
    @abstractmethod
    async def delete(self, customer_id: UUID) -> bool:
        """Eliminar cliente"""
        pass
    
    @abstractmethod
    async def activate(self, customer_id: UUID) -> Customer | None:
        """Activar cliente"""
        pass
    
    @abstractmethod
    async def deactivate(self, customer_id: UUID) -> Customer | None:
        """Desactivar cliente"""
        pass 