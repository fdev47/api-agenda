"""
Use case para obtener usuario por auth_uid
"""
from uuid import UUID
from ...domain.interfaces.user_repository import UserRepository
from ...domain.dto.responses.user_responses import UserResponse
from ...domain.exceptions.user_exceptions import UserNotFoundException


class GetUserByAuthUidUseCase:
    """Use case para obtener usuario por auth_uid"""
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, auth_uid: str) -> UserResponse:
        """Ejecutar el use case"""
        user = await self._user_repository.get_by_auth_uid(auth_uid)
        
        if not user:
            raise UserNotFoundException(f"auth_uid: {auth_uid}")
        
        return UserResponse.model_validate(user) 