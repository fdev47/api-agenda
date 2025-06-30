"""
Caso de uso para asignar permiso a un usuario
"""
from typing import Optional
from ...domain.interfaces.user_repository import UserRepository
from ...domain.exceptions.user_exceptions import UserNotFoundException


class AssignPermissionUseCase:
    """Caso de uso para asignar permiso a un usuario"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_id: str, permission: str) -> bool:
        """Ejecutar el caso de uso"""
        
        # Verificar que el usuario existe
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"Usuario con ID {user_id} no encontrado")
        
        # Asignar el permiso al usuario
        # Nota: Esta implementación dependerá de cómo se manejen los permisos en tu sistema
        # Por ahora, asumimos que se actualiza el usuario con el nuevo permiso
        # En un sistema real, esto podría involucrar una tabla de permisos o un campo JSON
        if not hasattr(user, 'permissions'):
            user.permissions = []
        
        if permission not in user.permissions:
            user.permissions.append(permission)
            await self.user_repository.update(user)
        
        return True 