"""
DTOs de respuesta del API Gateway
"""
from .user import (
    UserResponse, 
    UserListResponse, 
    RoleResponse,
    ProfileResponse,
    AddressResponse,
    CustomerResponse
)
from .common import SuccessResponse

__all__ = [
    "UserResponse", 
    "UserListResponse", 
    "RoleResponse",
    "ProfileResponse",
    "AddressResponse",
    "CustomerResponse",
    "SuccessResponse"
] 