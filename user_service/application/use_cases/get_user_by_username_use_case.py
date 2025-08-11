"""
Use case para obtener usuario por username
"""
from ...domain.interfaces.user_repository import UserRepository
from ...domain.dto.responses.user_responses import UserResponse
from ...domain.exceptions.user_exceptions import UserNotFoundException


class GetUserByUsernameUseCase:
    """Use case para obtener usuario por username"""
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, username: str) -> UserResponse:
        """Ejecutar el use case"""
        user = await self._user_repository.get_by_username(username)
        
        if not user:
            raise UserNotFoundException(f"username: {username}")
        
        return UserResponse.model_validate(user)
