"""
Use case para obtener perfil por ID
"""
from uuid import UUID
from typing import Optional
from ...domain.entities.profile import Profile
from ...domain.interfaces.profile_repository import IProfileRepository
from ...domain.exceptions.user_exceptions import ProfileNotFoundException


class GetProfileByIdUseCase:
    """Use case para obtener perfil por ID"""
    
    def __init__(self, profile_repository: IProfileRepository):
        self.profile_repository = profile_repository
    
    async def execute(self, profile_id: UUID) -> Optional[Profile]:
        """Ejecutar el use case"""
        profile = await self.profile_repository.get_by_id(profile_id)
        
        if not profile:
            raise ProfileNotFoundException(str(profile_id))
        
        return profile 