from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from ..entities.role import Role

class IRoleRepository(ABC):
    @abstractmethod
    async def get_by_id(self, role_id: UUID) -> Role | None:
        ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Role | None:
        ...

    @abstractmethod
    async def create(self, role: Role) -> Role:
        ...

    @abstractmethod
    async def update(self, role: Role) -> Role:
        ...

    @abstractmethod
    async def list_all(self) -> List[Role]:
        ...
