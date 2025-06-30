"""
Interfaz del repositorio de ciudades
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.city import City
from ..dto.requests.city_requests import CityFilterRequest

class CityRepository(ABC):
    """Interfaz para el repositorio de ciudades"""
    
    @abstractmethod
    async def create(self, city: City) -> City:
        """Crear una ciudad"""
        pass
    
    @abstractmethod
    async def get_by_id(self, city_id: int) -> Optional[City]:
        """Obtener ciudad por ID"""
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[City]:
        """Obtener ciudad por nombre"""
        pass
    
    @abstractmethod
    async def get_by_state_id(self, state_id: int) -> List[City]:
        """Obtener ciudades por estado"""
        pass
    
    @abstractmethod
    async def get_by_country_id(self, country_id: int) -> List[City]:
        """Obtener ciudades por país"""
        pass
    
    @abstractmethod
    async def get_all(self, filter_request: CityFilterRequest) -> tuple[List[City], int]:
        """Obtener todas las ciudades con filtros y paginación"""
        pass
    
    @abstractmethod
    async def update(self, city_id: int, city: City) -> Optional[City]:
        """Actualizar una ciudad"""
        pass
    
    @abstractmethod
    async def delete(self, city_id: int) -> bool:
        """Eliminar una ciudad"""
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe una ciudad con el nombre dado"""
        pass
    
    @abstractmethod
    async def exists_by_id(self, city_id: int) -> bool:
        """Verificar si existe una ciudad con el ID dado"""
        pass
    
    @abstractmethod
    async def exists_by_state_id(self, state_id: int) -> bool:
        """Verificar si existe un estado con el ID dado"""
        pass 