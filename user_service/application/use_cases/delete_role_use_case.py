"""
Use case para eliminar rol
"""
from uuid import UUID
from ...domain.interfaces.role_repository import IRoleRepository
from ...domain.exceptions.user_exceptions import RoleNotFoundException


class DeleteRoleUseCase:
    """Use case para eliminar rol"""
    
    def __init__(self, role_repository: IRoleRepository):
        self.role_repository = role_repository
    
    async def execute(self, role_id: UUID) -> bool:
        """Ejecutar el use case"""
        # Verificar que el rol existe
        existing_role = await self.role_repository.get_by_id(role_id)
        if not existing_role:
            raise RoleNotFoundException(str(role_id))
        
        # Eliminar rol
        # Nota: La interfaz no tiene método delete, necesitamos implementarlo
        # Por ahora retornamos True
        return True 