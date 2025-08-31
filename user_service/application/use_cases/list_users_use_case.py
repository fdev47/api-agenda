"""
Use case para listar usuarios
"""
from typing import List, Optional
from ...domain.interfaces.user_repository import UserRepository
from ...domain.dto.responses.user_responses import UserResponse, UserListResponse
from ...domain.entities.user import UserType


class ListUsersUseCase:
    """Use case para listar usuarios"""
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        username: Optional[str] = None,
        user_type: Optional[UserType] = None,
        branch_code: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> UserListResponse:
        """Ejecutar el use case"""
        users = await self._user_repository.list_users(
            skip=skip, 
            limit=limit, 
            username=username,
            user_type=user_type,
            branch_code=branch_code,
            is_active=is_active
        )
        
        user_responses = [UserResponse.model_validate(user) for user in users]
        
        return UserListResponse(
            users=user_responses,
            total=len(user_responses),
            page=skip // limit + 1 if limit > 0 else 1,
            size=limit
        ) 