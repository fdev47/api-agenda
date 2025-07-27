"""
Caso de uso para asignar roles a un perfil
"""
from typing import List
from uuid import UUID

from ...domain.interfaces.profile_repository import IProfileRepository
from ...domain.interfaces.role_repository import IRoleRepository
from ...domain.dto.responses import ProfileResponse
from ...domain.exceptions.user_exceptions import ProfileNotFoundException, RoleNotFoundException


class AssignRolesToProfileUseCase:
    """Caso de uso para asignar roles a un perfil"""
    
    def __init__(self, profile_repository: IProfileRepository, role_repository: IRoleRepository):
        self._profile_repository = profile_repository
        self._role_repository = role_repository
    
    async def execute(self, profile_id: UUID, role_ids: List[UUID]) -> ProfileResponse:
        """Ejecutar caso de uso de asignación de roles a perfil"""
        # Verificar que el perfil existe
        existing_profile = await self._profile_repository.get_by_id(profile_id)
        if not existing_profile:
            raise ProfileNotFoundException(str(profile_id))
        
        # Verificar que todos los roles existan
        for role_id in role_ids:
            role = await self._role_repository.get_by_id(role_id)
            if not role:
                raise RoleNotFoundException(str(role_id))
        
        # Asignar roles al perfil
        updated_profile = await self._profile_repository.assign_roles(profile_id, role_ids)
        
        return ProfileResponse.from_orm(updated_profile) 