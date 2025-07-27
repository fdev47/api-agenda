"""
Use case para actualizar perfil
"""
from uuid import UUID
from typing import Optional
from ...domain.entities.profile import Profile
from ...domain.interfaces.profile_repository import IProfileRepository
from ...domain.dto.requests.profile_requests import UpdateProfileRequest
from ...domain.exceptions.user_exceptions import ProfileNotFoundException


class UpdateProfileUseCase:
    """Use case para actualizar perfil"""
    
    def __init__(self, profile_repository: IProfileRepository):
        self.profile_repository = profile_repository
    
    async def execute(self, profile_id: UUID, request: UpdateProfileRequest) -> Optional[Profile]:
        """Ejecutar el use case"""
        # Verificar que el perfil existe
        existing_profile = await self.profile_repository.get_by_id(profile_id)
        if not existing_profile:
            raise ProfileNotFoundException(str(profile_id))
        
        # Actualizar perfil
        updated_profile = await self.profile_repository.update(existing_profile)
        return updated_profile 