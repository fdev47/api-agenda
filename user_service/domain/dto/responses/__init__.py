"""
DTOs de responses para el dominio de usuarios
"""
from .user_responses import UserResponse, UserListResponse, UserType
from .profile_responses import ProfileResponse, ProfileListResponse
from .role_responses import RoleResponse, RoleListResponse
from .customer_responses import CustomerResponse, CustomerListResponse
from .address_responses import (
    AddressResponse, 
    AddressListResponse, 
    AddressCreatedResponse,
    AddressUpdatedResponse,
    AddressDeletedResponse
)
from .error_responses import ErrorResponse, ValidationErrorResponse
from .success_responses import SuccessResponse, MessageResponse, RoleAssignmentResponse, PermissionAssignmentResponse, UserRolesResponse

__all__ = [
    'UserResponse',
    'UserListResponse',
    'UserType',
    'ProfileResponse',
    'ProfileListResponse',
    'RoleResponse',
    'RoleListResponse',
    'CustomerResponse',
    'CustomerListResponse',
    'AddressResponse',
    'AddressListResponse',
    'AddressCreatedResponse',
    'AddressUpdatedResponse',
    'AddressDeletedResponse',
    'ErrorResponse',
    'ValidationErrorResponse',
    'SuccessResponse',
    'MessageResponse',
    'RoleAssignmentResponse',
    'PermissionAssignmentResponse',
    'UserRolesResponse'
] 