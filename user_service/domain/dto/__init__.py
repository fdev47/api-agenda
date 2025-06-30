"""
Data Transfer Objects para el dominio de usuarios
"""
from .requests import (
    CreateUserRequest, UpdateUserRequest, UserType,
    CreateProfileRequest, UpdateProfileRequest,
    CreateRoleRequest, UpdateRoleRequest
)
from .responses import (
    UserResponse, UserListResponse,
    ProfileResponse, RoleResponse
)

__all__ = [
    # Requests
    'CreateUserRequest',
    'UpdateUserRequest', 
    'UserType',
    'CreateProfileRequest',
    'UpdateProfileRequest',
    'CreateRoleRequest',
    'UpdateRoleRequest',
    # Responses
    'UserResponse',
    'UserListResponse',
    'ProfileResponse',
    'RoleResponse'
] 