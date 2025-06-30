"""
Interfaz del repositorio para sectores
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.sector import Sector
from ..dto.requests.sector_requests import SectorFilterRequest


class SectorRepository(ABC):
    """Interfaz del repositorio para sectores"""
    
    @abstractmethod
    async def create(self, sector: Sector) -> Sector:
        """Crear un nuevo sector"""
        pass
    
    @abstractmethod
    async def get_by_id(self, sector_id: int) -> Optional[Sector]:
        """Obtener un sector por ID"""
        pass
    
    @abstractmethod
    async def get_by_branch_id(self, branch_id: int) -> List[Sector]:
        """Obtener todos los sectores de una sucursal"""
        pass
    
    @abstractmethod
    async def list(self, filter_request: SectorFilterRequest) -> tuple[List[Sector], int]:
        """Listar sectores con filtros y paginación"""
        pass
    
    @abstractmethod
    async def update(self, sector: Sector) -> Sector:
        """Actualizar un sector"""
        pass
    
    @abstractmethod
    async def delete(self, sector_id: int) -> bool:
        """Eliminar un sector"""
        pass
    
    @abstractmethod
    async def exists_by_name_and_branch(self, name: str, branch_id: int, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un sector con el mismo nombre en la misma sucursal"""
        pass 