"""
Use case para obtener usuario por email
"""
from ...domain.interfaces.user_repository import UserRepository
from ...domain.dto.responses.user_responses import UserResponse
from ...domain.exceptions.user_exceptions import UserNotFoundException


class GetUserByEmailUseCase:
    """Use case para obtener usuario por email"""
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, email: str) -> UserResponse:
        """Ejecutar el use case"""
        user = await self._user_repository.get_by_email(email)
        
        if not user:
            raise UserNotFoundException(f"email: {email}")
        
        return UserResponse.model_validate(user) 