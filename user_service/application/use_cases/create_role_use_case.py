"""
Caso de uso para crear roles
"""
from ...domain.interfaces.role_repository import IRoleRepository
from ...domain.entities import Role
from ...domain.dto.requests import CreateRoleRequest
from ...domain.dto.responses import RoleResponse
from ...domain.exceptions.user_exceptions import RoleAlreadyExistsException


class CreateRoleUseCase:
    """Caso de uso para crear roles"""
    
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository
    
    async def execute(self, request: CreateRoleRequest) -> RoleResponse:
        """Ejecutar caso de uso de creación de rol"""
        # Verificar que el nombre no exista
        existing_role = await self._role_repository.get_by_name(request.name)
        if existing_role:
            raise RoleAlreadyExistsException(request.name)
        
        # Crear rol
        role = Role(
            name=request.name,
            description=request.description
        )
        
        created_role = await self._role_repository.create(role)
        return RoleResponse.from_orm(created_role) 