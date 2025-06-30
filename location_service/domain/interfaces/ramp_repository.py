"""
Interfaz del repositorio para rampas
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.ramp import Ramp
from ..dto.requests.ramp_requests import RampFilterRequest


class RampRepository(ABC):
    """Interfaz del repositorio para rampas"""
    
    @abstractmethod
    async def create(self, ramp: Ramp) -> Ramp:
        """Crear una nueva rampa"""
        pass
    
    @abstractmethod
    async def get_by_id(self, ramp_id: int) -> Optional[Ramp]:
        """Obtener una rampa por ID"""
        pass
    
    @abstractmethod
    async def get_by_branch_id(self, branch_id: int) -> List[Ramp]:
        """Obtener todas las rampas de una sucursal"""
        pass
    
    @abstractmethod
    async def list(self, filter_request: RampFilterRequest) -> tuple[List[Ramp], int]:
        """Listar rampas con filtros y paginación"""
        pass
    
    @abstractmethod
    async def update(self, ramp: Ramp) -> Ramp:
        """Actualizar una rampa"""
        pass
    
    @abstractmethod
    async def delete(self, ramp_id: int) -> bool:
        """Eliminar una rampa"""
        pass
    
    @abstractmethod
    async def exists_by_name_and_branch(self, name: str, branch_id: int, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe una rampa con el mismo nombre en la misma sucursal"""
        pass 