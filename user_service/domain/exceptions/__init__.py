"""
Excepciones del dominio de usuarios
"""

from .user_exceptions import (
    UserException,
    UserNotFoundException,
    UserAlreadyExistsException,
    UserFirebaseUIDAlreadyExistsException,
    ProfileNotFoundException,
    ProfileAlreadyExistsException,
    RoleNotFoundException,
    RoleAlreadyExistsException,
    InvalidUserDataException,
    UserInactiveException,
    UserValidationException
)

# Alias para compatibilidad
UserError = UserException

__all__ = [
    "UserException",
    "UserError",  # Alias
    "UserNotFoundException",
    "UserAlreadyExistsException",
    "UserFirebaseUIDAlreadyExistsException",
    "ProfileNotFoundException",
    "ProfileAlreadyExistsException",
    "RoleNotFoundException",
    "RoleAlreadyExistsException",
    "InvalidUserDataException",
    "UserInactiveException",
    "UserValidationException"
] 