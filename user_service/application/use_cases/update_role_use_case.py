"""
Use case para actualizar rol
"""
from uuid import UUID
from typing import Optional
from ...domain.entities.role import Role
from ...domain.interfaces.role_repository import IRoleRepository
from ...domain.dto.requests.role_requests import UpdateRoleRequest
from ...domain.exceptions.user_exceptions import RoleNotFoundException


class UpdateRoleUseCase:
    """Use case para actualizar rol"""
    
    def __init__(self, role_repository: IRoleRepository):
        self.role_repository = role_repository
    
    async def execute(self, role_id: UUID, request: UpdateRoleRequest) -> Optional[Role]:
        """Ejecutar el use case"""
        # Verificar que el rol existe
        existing_role = await self.role_repository.get_by_id(role_id)
        if not existing_role:
            raise RoleNotFoundException(str(role_id))
        
        # Actualizar rol
        updated_role = await self.role_repository.update(existing_role)
        return updated_role 