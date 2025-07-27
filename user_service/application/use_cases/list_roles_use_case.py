"""
Use case para listar roles
"""
from typing import List
from ...domain.entities.role import Role
from ...domain.interfaces.role_repository import IRoleRepository


class ListRolesUseCase:
    """Use case para listar roles"""
    
    def __init__(self, role_repository: IRoleRepository):
        self.role_repository = role_repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """Ejecutar el use case"""
        roles = await self.role_repository.list_all()
        return roles[skip:skip + limit] 