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
        
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"Usuario con ID {user_id} no encontrado")
        
        roles = []
        
        if hasattr(user, 'role_id') and user.role_id:
            role = await self.role_repository.get_by_id(user.role_id)
            if role:
                roles.append(role.name)
        
        # Si el usuario tiene roles adicionales
        if hasattr(user, 'roles') and user.roles:
            roles.extend(user.roles)
        
        return roles 