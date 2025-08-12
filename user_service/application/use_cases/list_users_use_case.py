"""
Use case para listar usuarios
"""
from typing import List
from ...domain.interfaces.user_repository import UserRepository
from ...domain.dto.responses.user_responses import UserResponse, UserListResponse


class ListUsersUseCase:
    """Use case para listar usuarios"""
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, skip: int = 0, limit: int = 100, branch_code: str = None) -> UserListResponse:
        """Ejecutar el use case"""
        users = await self._user_repository.list_users(skip, limit, branch_code)
        
        user_responses = [UserResponse.model_validate(user) for user in users]
        
        return UserListResponse(
            users=user_responses,
            total=len(user_responses),
            page=skip // limit + 1 if limit > 0 else 1,
            size=limit
        ) 