"""
Interfaz del repositorio para unidades de medida
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.measurement_unit_entity import MeasurementUnit
from ..dto.requests.measurement_unit_requests import MeasurementUnitFilterRequest


class MeasurementUnitRepository(ABC):
    """Interfaz del repositorio para unidades de medida"""
    
    @abstractmethod
    async def create(self, measurement_unit: MeasurementUnit) -> MeasurementUnit:
        """Crear una nueva unidad de medida"""
        pass
    
    @abstractmethod
    async def get_by_id(self, measurement_unit_id: int) -> Optional[MeasurementUnit]:
        """Obtener una unidad de medida por ID"""
        pass
    
    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[MeasurementUnit]:
        """Obtener una unidad de medida por código"""
        pass
    
    @abstractmethod
    async def list_all(self, filter_request: MeasurementUnitFilterRequest) -> tuple[List[MeasurementUnit], int]:
        """Listar todas las unidades de medida con filtros"""
        pass
    
    @abstractmethod
    async def update(self, measurement_unit_id: int, measurement_unit: MeasurementUnit) -> Optional[MeasurementUnit]:
        """Actualizar una unidad de medida"""
        pass
    
    @abstractmethod
    async def delete(self, measurement_unit_id: int) -> bool:
        """Eliminar una unidad de medida"""
        pass
    
    @abstractmethod
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe una unidad de medida con el código dado"""
        pass
    
    @abstractmethod
    async def exists_by_id(self, measurement_unit_id: int) -> bool:
        """Verificar si existe una unidad de medida con el ID dado"""
        pass 