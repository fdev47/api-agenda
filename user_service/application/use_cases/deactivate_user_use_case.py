"""
Use case para desactivar usuario
"""
from uuid import UUID
from ...domain.interfaces.user_repository import UserRepository
from ...domain.dto.responses.user_responses import UserResponse
from ...domain.exceptions.user_exceptions import UserNotFoundException


class DeactivateUserUseCase:
    """Use case para desactivar usuario"""
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, user_id: UUID) -> UserResponse:
        """Ejecutar el use case"""
        # Verificar que el usuario existe
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"user_id: {user_id}")
        
        # Desactivar usuario
        deactivated_user = await self._user_repository.deactivate(user_id)
        
        if not deactivated_user:
            raise UserNotFoundException(f"user_id: {user_id}")
        
        return UserResponse.model_validate(deactivated_user) 