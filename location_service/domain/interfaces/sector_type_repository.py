"""
Interfaz del repositorio para tipos de sector
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.sector_type import SectorType
from ..dto.requests.sector_type_requests import SectorTypeFilterRequest

class SectorTypeRepository(ABC):
    @abstractmethod
    async def create(self, sector_type: SectorType) -> SectorType:
        pass

    @abstractmethod
    async def get_by_id(self, sector_type_id: int) -> Optional[SectorType]:
        pass

    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[SectorType]:
        pass

    @abstractmethod
    async def list(self, filter_request: SectorTypeFilterRequest) -> tuple[List[SectorType], int]:
        pass

    @abstractmethod
    async def update(self, sector_type: SectorType) -> SectorType:
        pass

    @abstractmethod
    async def delete(self, sector_type_id: int) -> bool:
        pass

    @abstractmethod
    async def exists_by_name_or_code(self, name: str, code: str, exclude_id: Optional[int] = None) -> bool:
        pass 