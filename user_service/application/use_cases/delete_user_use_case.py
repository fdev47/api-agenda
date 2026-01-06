"""
Use case para eliminar usuario
"""
from uuid import UUID
from ...domain.interfaces.user_repository import UserRepository
from ...domain.exceptions.user_exceptions import UserNotFoundException


class DeleteUserUseCase:
    """Use case para eliminar usuario"""
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, user_id: UUID) -> bool:
        """Ejecutar el use case"""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"user_id: {user_id}")
        
        return await self._user_repository.delete(user_id) 