"""
Interfaz del repositorio de países
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.country import Country
from ..dto.requests.country_requests import CountryFilterRequest

class CountryRepository(ABC):
    """Interfaz para el repositorio de países"""
    
    @abstractmethod
    async def create(self, country: Country) -> Country:
        """Crear un país"""
        pass
    
    @abstractmethod
    async def get_by_id(self, country_id: int) -> Optional[Country]:
        """Obtener país por ID"""
        pass
    
    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[Country]:
        """Obtener país por código ISO"""
        pass
    
    @abstractmethod
    async def get_all(self, filter_request: CountryFilterRequest) -> tuple[List[Country], int]:
        """Obtener todos los países con filtros y paginación"""
        pass
    
    @abstractmethod
    async def update(self, country_id: int, country: Country) -> Optional[Country]:
        """Actualizar un país"""
        pass
    
    @abstractmethod
    async def delete(self, country_id: int) -> bool:
        """Eliminar un país"""
        pass
    
    @abstractmethod
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un país con el código dado"""
        pass
    
    @abstractmethod
    async def exists_by_id(self, country_id: int) -> bool:
        """Verificar si existe un país con el ID dado"""
        pass 