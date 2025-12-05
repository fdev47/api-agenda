"""
Excepciones del dominio de usuarios
"""
from typing import Any, Dict, List, Optional


class UserException(Exception):
    """Excepción base para errores de usuarios"""
    
    def __init__(self, message: str, error_code: str = "USER_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class UserNotFoundException(UserException):
    """Excepción cuando no se encuentra un usuario"""
    
    def __init__(self, message: str = "Usuario no encontrado"):
        super().__init__(message, "USER_NOT_FOUND")


class UserAlreadyExistsException(UserException):
    """Excepción cuando el usuario ya existe"""
    
    def __init__(self, auth_uid: str):
        super().__init__(f"Usuario con auth_uid {auth_uid} ya existe", "AUTH_UID_ALREADY_EXISTS")


class InvalidUserDataException(UserException):
    """Excepción cuando los datos del usuario son inválidos"""
    
    def __init__(self, message: str = "Datos de usuario inválidos"):
        super().__init__(message, "INVALID_USER_DATA")


class UserValidationException(UserException):
    """Excepción cuando falla la validación del usuario"""
    
    def __init__(self, errors: List[str]):
        message = f"Errores de validación: {', '.join(errors)}"
        super().__init__(message, "USER_VALIDATION_ERROR")
        self.errors = errors

class UserFirebaseUIDAlreadyExistsException(UserException):
    """Excepción cuando el Firebase UID ya existe"""
    def __init__(self, firebase_uid: str):
        super().__init__(f"Usuario con Firebase UID {firebase_uid} ya existe", "FIREBASE_UID_ALREADY_EXISTS")

class ProfileNotFoundException(UserException):
    """Excepción cuando no se encuentra un perfil"""
    def __init__(self, profile_id: str):
        super().__init__(f"Perfil con ID {profile_id} no encontrado", "PROFILE_NOT_FOUND")

class ProfileAlreadyExistsException(UserException):
    """Excepción cuando el perfil ya existe"""
    def __init__(self, name: str):
        super().__init__(f"Perfil con nombre {name} ya existe", "PROFILE_ALREADY_EXISTS")

class RoleNotFoundException(UserException):
    """Excepción cuando no se encuentra un rol"""
    def __init__(self, role_id: str):
        super().__init__(f"Rol con ID {role_id} no encontrado", "ROLE_NOT_FOUND")

class RoleAlreadyExistsException(UserException):
    """Excepción cuando el rol ya existe"""
    def __init__(self, name: str):
        super().__init__(f"Rol con nombre {name} ya existe", "ROLE_ALREADY_EXISTS")

class UserInactiveException(UserException):
    """Excepción cuando el usuario está inactivo"""
    def __init__(self, user_id: str):
        super().__init__(f"Usuario con ID {user_id} está inactivo", "USER_INACTIVE")


# Excepciones para Customer
class CustomerAlreadyExistsException(UserException):
    """Excepción cuando el customer ya existe"""
    def __init__(self, field: str, value: str):
        super().__init__(f"Proveedor con {field} '{value}' ya existe", f"CUSTOMER_{field.upper()}_ALREADY_EXISTS")
        self.field = field
        self.value = value


class CustomerAuthUidAlreadyExistsException(UserException):
    """Excepción cuando el auth_uid del customer ya existe"""
    def __init__(self, auth_uid: str):
        super().__init__(f"Proveedor con auth_uid '{auth_uid}' ya existe", "CUSTOMER_AUTH_UID_ALREADY_EXISTS")


class CustomerRucAlreadyExistsException(UserException):
    """Excepción cuando el RUC del customer ya existe"""
    def __init__(self, ruc: str):
        super().__init__(f"Proveedor con RUC '{ruc}' ya existe", "CUSTOMER_RUC_ALREADY_EXISTS")


class CustomerEmailAlreadyExistsException(UserException):
    """Excepción cuando el email del customer ya existe"""
    def __init__(self, email: str):
        super().__init__(f"Proveedor con email '{email}' ya existe", "CUSTOMER_EMAIL_ALREADY_EXISTS")


class CustomerUsernameAlreadyExistsException(UserException):
    """Excepción cuando el username del customer ya existe"""
    def __init__(self, username: str):
        super().__init__(f"Proveedor con username '{username}' ya existe", "CUSTOMER_USERNAME_ALREADY_EXISTS")


class CustomerNotFoundException(UserException):
    """Excepción cuando no se encuentra un customer"""
    def __init__(self, message: str = "Proveedor no encontrado"):
        super().__init__(message, "CUSTOMER_NOT_FOUND") 