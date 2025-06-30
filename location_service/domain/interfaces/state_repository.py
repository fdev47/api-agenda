"""
Interfaz del repositorio de estados
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.state import State
from ..dto.requests.state_requests import StateFilterRequest

class StateRepository(ABC):
    """Interfaz para el repositorio de estados"""
    
    @abstractmethod
    async def create(self, state: State) -> State:
        """Crear un estado"""
        pass
    
    @abstractmethod
    async def get_by_id(self, state_id: int) -> Optional[State]:
        """Obtener estado por ID"""
        pass
    
    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[State]:
        """Obtener estado por código"""
        pass
    
    @abstractmethod
    async def get_by_country_id(self, country_id: int) -> List[State]:
        """Obtener estados por país"""
        pass
    
    @abstractmethod
    async def get_all(self, filter_request: StateFilterRequest) -> tuple[List[State], int]:
        """Obtener todos los estados con filtros y paginación"""
        pass
    
    @abstractmethod
    async def update(self, state_id: int, state: State) -> Optional[State]:
        """Actualizar un estado"""
        pass
    
    @abstractmethod
    async def delete(self, state_id: int) -> bool:
        """Eliminar un estado"""
        pass
    
    @abstractmethod
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un estado con el código dado"""
        pass
    
    @abstractmethod
    async def exists_by_id(self, state_id: int) -> bool:
        """Verificar si existe un estado con el ID dado"""
        pass
    
    @abstractmethod
    async def exists_by_country_id(self, country_id: int) -> bool:
        """Verificar si existe un país con el ID dado"""
        pass 