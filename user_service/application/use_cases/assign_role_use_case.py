"""
Caso de uso para asignar rol a un usuario
"""
from typing import Optional
from ...domain.interfaces.user_repository import UserRepository
from ...domain.interfaces.role_repository import IRoleRepository
from ...domain.exceptions.user_exceptions import UserNotFoundException, RoleNotFoundException


class AssignRoleUseCase:
    """Caso de uso para asignar rol a un usuario"""
    
    def __init__(self, user_repository: UserRepository, role_repository: IRoleRepository):
        self.user_repository = user_repository
        self.role_repository = role_repository
    
    async def execute(self, user_id: str, role_name: str) -> bool:
        """Ejecutar el caso de uso"""
        
        # Verificar que el usuario existe
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"Usuario con ID {user_id} no encontrado")
        
        # Verificar que el rol existe
        role = await self.role_repository.get_by_name(role_name)
        if not role:
            raise RoleNotFoundException(f"Rol '{role_name}' no encontrado")
        
        # Asignar el rol al usuario
        # Nota: Esta implementación dependerá de cómo se manejen los roles en tu sistema
        # Por ahora, asumimos que se actualiza el usuario con el nuevo rol
        user.role_id = role.id
        await self.user_repository.update(user)
        
        return True 