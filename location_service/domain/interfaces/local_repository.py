"""
Interfaz del repositorio para locales
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.local import Local
from ..dto.requests.local_requests import LocalFilterRequest


class LocalRepository(ABC):
    """Interfaz del repositorio para locales"""
    
    @abstractmethod
    async def create(self, local: Local) -> Local:
        """Crear un nuevo local"""
        pass
    
    @abstractmethod
    async def get_by_id(self, local_id: int) -> Optional[Local]:
        """Obtener un local por ID"""
        pass
    
    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[Local]:
        """Obtener un local por código"""
        pass
    
    @abstractmethod
    async def list_all(self, filter_request: LocalFilterRequest) -> tuple[List[Local], int]:
        """Listar todos los locales con filtros"""
        pass
    
    @abstractmethod
    async def update(self, local_id: int, local: Local) -> Optional[Local]:
        """Actualizar un local"""
        pass
    
    @abstractmethod
    async def delete(self, local_id: int) -> bool:
        """Eliminar un local"""
        pass
    
    @abstractmethod
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un local con el código dado"""
        pass
    
    @abstractmethod
    async def exists_by_id(self, local_id: int) -> bool:
        """Verificar si existe un local con el ID dado"""
        pass 