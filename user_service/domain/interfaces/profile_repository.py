from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from ..entities.profile import Profile

class IProfileRepository(ABC):
    @abstractmethod
    async def get_by_id(self, profile_id: UUID) -> Profile | None:
        ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Profile | None:
        ...

    @abstractmethod
    async def create(self, profile: Profile) -> Profile:
        ...

    @abstractmethod
    async def update(self, profile: Profile) -> Profile:
        ...

    @abstractmethod
    async def list_all(self) -> List[Profile]:
        ...
