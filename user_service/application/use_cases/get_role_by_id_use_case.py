"""
Use case para obtener rol por ID
"""
from uuid import UUID
from typing import Optional
from ...domain.entities.role import Role
from ...domain.interfaces.role_repository import IRoleRepository
from ...domain.exceptions.user_exceptions import RoleNotFoundException


class GetRoleByIdUseCase:
    """Use case para obtener rol por ID"""
    
    def __init__(self, role_repository: IRoleRepository):
        self.role_repository = role_repository
    
    async def execute(self, role_id: UUID) -> Optional[Role]:
        """Ejecutar el use case"""
        role = await self.role_repository.get_by_id(role_id)
        
        if not role:
            raise RoleNotFoundException(str(role_id))
        
        return role 