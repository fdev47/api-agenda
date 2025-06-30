"""
Use case para actualizar usuario
"""
from uuid import UUID
from ...domain.interfaces.user_repository import UserRepository
from ...domain.dto.requests.user_requests import UpdateUserRequest
from ...domain.dto.responses.user_responses import UserResponse
from ...domain.exceptions.user_exceptions import UserNotFoundException


class UpdateUserUseCase:
    """Use case para actualizar usuario"""
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, user_id: UUID, user_data: UpdateUserRequest) -> UserResponse:
        """Ejecutar el use case"""
        # Verificar que el usuario existe
        existing_user = await self._user_repository.get_by_id(user_id)
        if not existing_user:
            raise UserNotFoundException(f"user_id: {user_id}")
        
        # Actualizar usuario
        updated_user = await self._user_repository.update(user_id, user_data)
        
        if not updated_user:
            raise UserNotFoundException(f"user_id: {user_id}")
        
        return UserResponse.model_validate(updated_user) 