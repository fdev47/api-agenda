"""
Caso de uso para obtener roles de un usuario
"""
from typing import List
from ...domain.interfaces.user_repository import UserRepository
from ...domain.interfaces.role_repository import IRoleRepository
from ...domain.exceptions.user_exceptions import UserNotFoundException


class GetUserRolesUseCase:
    """Caso de uso para obtener roles de un usuario"""
    
    def __init__(self, user_repository: UserRepository, role_repository: IRoleRepository):
        self.user_repository = user_repository
        self.role_repository = role_repository
    
    async def execute(self, user_id: str) -> List[str]:
        """Ejecutar el caso de uso"""
        
        # Verificar que el usuario existe
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"Usuario con ID {user_id} no encontrado")
        
        # Obtener los roles del usuario
        # Nota: Esta implementación dependerá de cómo se manejen los roles en tu sistema
        # Por ahora, asumimos que el usuario tiene un rol asignado
        roles = []
        
        if hasattr(user, 'role_id') and user.role_id:
            role = await self.role_repository.get_by_id(user.role_id)
            if role:
                roles.append(role.name)
        
        # Si el usuario tiene roles adicionales (por ejemplo, en un campo JSON o tabla separada)
        if hasattr(user, 'roles') and user.roles:
            roles.extend(user.roles)
        
        return roles 