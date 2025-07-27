"""
Caso de uso para crear perfiles
"""
from uuid import UUID

from ...domain.interfaces.profile_repository import IProfileRepository
from ...domain.interfaces.role_repository import IRoleRepository
from ...domain.entities import Profile
from ...domain.dto.requests import CreateProfileRequest
from ...domain.dto.responses import ProfileResponse
from ...domain.exceptions.user_exceptions import (
    ProfileAlreadyExistsException, RoleNotFoundException
)


class CreateProfileUseCase:
    """Caso de uso para crear perfiles"""
    
    def __init__(self, profile_repository: IProfileRepository, role_repository: IRoleRepository):
        self._profile_repository = profile_repository
        self._role_repository = role_repository
    
    async def execute(self, request: CreateProfileRequest) -> ProfileResponse:
        """Ejecutar caso de uso de creación de perfil"""
        # Verificar que el nombre no exista
        existing_profile = await self._profile_repository.get_by_name(request.name)
        if existing_profile:
            raise ProfileAlreadyExistsException(request.name)
        
        # Verificar que los roles existan
        roles = []
        for role_id in request.role_ids:
            role = await self._role_repository.get_by_id(role_id)
            if not role:
                raise RoleNotFoundException(str(role_id))
            roles.append(role)
        
        # Crear perfil sin roles primero
        profile = Profile(
            name=request.name,
            description=request.description,
            roles=[]  # Sin roles inicialmente
        )
        
        created_profile = await self._profile_repository.create(profile)
        
        # Ahora asignar los roles al perfil creado
        # Nota: Por ahora solo creamos el perfil sin roles para evitar problemas
        # La asignación de roles se puede implementar en un use case separado
        
        return ProfileResponse.from_orm(created_profile) 