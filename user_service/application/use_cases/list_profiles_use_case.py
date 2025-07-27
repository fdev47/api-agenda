"""
Use case para listar perfiles
"""
from typing import List
from ...domain.entities.profile import Profile
from ...domain.interfaces.profile_repository import IProfileRepository


class ListProfilesUseCase:
    """Use case para listar perfiles"""
    
    def __init__(self, profile_repository: IProfileRepository):
        self.profile_repository = profile_repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> List[Profile]:
        """Ejecutar el use case"""
        profiles = await self.profile_repository.list_all()
        return profiles[skip:skip + limit] 