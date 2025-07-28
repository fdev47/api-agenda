"""
Interfaz del repositorio para sucursales
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.branch import Branch
from ..dto.requests.branch_requests import BranchFilterRequest


class BranchRepository(ABC):
    """Interfaz del repositorio para sucursales"""
    
    @abstractmethod
    async def create(self, branch: Branch) -> Branch:
        """Crear una nueva sucursal"""
        pass
    
    @abstractmethod
    async def get_by_id(self, branch_id: int) -> Optional[Branch]:
        """Obtener una sucursal por ID"""
        pass
    
    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[Branch]:
        """Obtener una sucursal por código"""
        pass
    
    @abstractmethod
    async def list_all(self, filter_request: BranchFilterRequest) -> tuple[List[Branch], int]:
        """Listar todas las sucursales con filtros"""
        pass
    
    @abstractmethod
    async def list_by_local(self, local_id: int) -> List[Branch]:
        """Listar sucursales por local"""
        pass
    
    @abstractmethod
    async def update(self, branch_id: int, branch: Branch) -> Optional[Branch]:
        """Actualizar una sucursal"""
        pass
    
    @abstractmethod
    async def delete(self, branch_id: int) -> bool:
        """Eliminar una sucursal"""
        pass
    
    @abstractmethod
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe una sucursal con el código dado"""
        pass
    
    @abstractmethod
    async def exists_by_id(self, branch_id: int) -> bool:
        """Verificar si existe una sucursal con el ID dado"""
        pass
    
    @abstractmethod
    async def exists_by_local_id(self, local_id: int) -> bool:
        """Verificar si existe un local con el ID dado"""
        pass
    
    @abstractmethod
    async def get_branch_with_relations(self, branch_id: int) -> Optional[dict]:
        """Obtener una sucursal con todas sus relaciones"""
        pass 