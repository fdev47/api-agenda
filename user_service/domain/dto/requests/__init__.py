"""
DTOs de requests para el dominio de usuarios
"""
from .user_requests import CreateUserRequest, UpdateUserRequest, UserType
from .profile_requests import CreateProfileRequest, UpdateProfileRequest
from .role_requests import CreateRoleRequest, UpdateRoleRequest
from .customer_requests import CreateCustomerRequest, UpdateCustomerRequest
from .address_requests import CreateAddressRequest, UpdateAddressRequest

__all__ = [
    'CreateUserRequest',
    'UpdateUserRequest', 
    'UserType',
    'CreateProfileRequest',
    'UpdateProfileRequest',
    'CreateRoleRequest',
    'UpdateRoleRequest',
    'CreateCustomerRequest',
    'UpdateCustomerRequest',
    'CreateAddressRequest',
    'UpdateAddressRequest'
] 