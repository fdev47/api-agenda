"""
Códigos de error estándar para todos los servicios
"""
from enum import Enum


class ErrorCode(Enum):
    """Códigos de error estándar"""
    
    # Errores de autenticación (1xxx)
    MISSING_TOKEN = "AUTH_001"
    INVALID_TOKEN = "AUTH_002"
    EXPIRED_TOKEN = "AUTH_003"
    INSUFFICIENT_PERMISSIONS = "AUTH_004"
    
    # Errores de validación (2xxx)
    VALIDATION_ERROR = "VALID_001"
    INVALID_DATE_FORMAT = "VALID_002"
    INVALID_EMAIL_FORMAT = "VALID_003"
    INVALID_UUID_FORMAT = "VALID_004"
    
    # Errores de recursos no encontrados (3xxx)
    USER_NOT_FOUND = "NOT_FOUND_001"
    CUSTOMER_NOT_FOUND = "NOT_FOUND_002"
    PROFILE_NOT_FOUND = "NOT_FOUND_003"
    ROLE_NOT_FOUND = "NOT_FOUND_004"
    COUNTRY_NOT_FOUND = "NOT_FOUND_005"
    STATE_NOT_FOUND = "NOT_FOUND_006"
    CITY_NOT_FOUND = "NOT_FOUND_007"
    RESERVATION_NOT_FOUND = "NOT_FOUND_008"
    
    # Errores de recursos duplicados (4xxx)
    USER_ALREADY_EXISTS = "DUPLICATE_001"
    CUSTOMER_ALREADY_EXISTS = "DUPLICATE_002"
    PROFILE_ALREADY_EXISTS = "DUPLICATE_003"
    ROLE_ALREADY_EXISTS = "DUPLICATE_004"
    EMAIL_ALREADY_EXISTS = "DUPLICATE_005"
    
    # Errores de base de datos (5xxx)
    DATABASE_CONNECTION_ERROR = "DB_001"
    DATABASE_QUERY_ERROR = "DB_002"
    DATABASE_TRANSACTION_ERROR = "DB_003"
    
    # Errores de servicios externos (6xxx)
    FIREBASE_ERROR = "EXTERNAL_001"
    USER_SERVICE_ERROR = "EXTERNAL_002"
    LOCATION_SERVICE_ERROR = "EXTERNAL_003"
    RESERVATION_SERVICE_ERROR = "EXTERNAL_004"
    AUTH_SERVICE_ERROR = "EXTERNAL_005"
    
    # Errores de comunicación (7xxx)
    SERVICE_UNAVAILABLE = "COMM_001"
    TIMEOUT_ERROR = "COMM_002"
    NETWORK_ERROR = "COMM_003"
    
    # Errores internos del servidor (9xxx)
    INTERNAL_SERVER_ERROR = "INTERNAL_001"
    UNEXPECTED_ERROR = "INTERNAL_002"
    CONFIGURATION_ERROR = "INTERNAL_003"


def get_error_code_by_exception(exception: Exception) -> str:
    """Obtener código de error basado en el tipo de excepción"""
    
    exception_name = exception.__class__.__name__
    
    # Mapeo de excepciones a códigos de error
    error_mapping = {
        # Excepciones de autenticación
        "UserNotFoundException": ErrorCode.USER_NOT_FOUND.value,
        "CustomerNotFoundException": ErrorCode.CUSTOMER_NOT_FOUND.value,
        "ProfileNotFoundException": ErrorCode.PROFILE_NOT_FOUND.value,
        "RoleNotFoundException": ErrorCode.ROLE_NOT_FOUND.value,
        "CountryNotFoundException": ErrorCode.COUNTRY_NOT_FOUND.value,
        "StateNotFoundException": ErrorCode.STATE_NOT_FOUND.value,
        "CityNotFoundException": ErrorCode.CITY_NOT_FOUND.value,
        "ReservationNotFoundException": ErrorCode.RESERVATION_NOT_FOUND.value,
        
        # Excepciones de duplicados
        "UserAlreadyExistsException": ErrorCode.USER_ALREADY_EXISTS.value,
        "CustomerAlreadyExistsException": ErrorCode.CUSTOMER_ALREADY_EXISTS.value,
        "ProfileAlreadyExistsException": ErrorCode.PROFILE_ALREADY_EXISTS.value,
        "RoleAlreadyExistsException": ErrorCode.ROLE_ALREADY_EXISTS.value,
        "EmailAlreadyExistsException": ErrorCode.EMAIL_ALREADY_EXISTS.value,
        
        # Excepciones de validación
        "ValidationError": ErrorCode.VALIDATION_ERROR.value,
        "InvalidDateFormatException": ErrorCode.INVALID_DATE_FORMAT.value,
        "InvalidEmailFormatException": ErrorCode.INVALID_EMAIL_FORMAT.value,
        "InvalidUUIDFormatException": ErrorCode.INVALID_UUID_FORMAT.value,
        
        # Excepciones de servicios externos
        "FirebaseError": ErrorCode.FIREBASE_ERROR.value,
        "UserServiceError": ErrorCode.USER_SERVICE_ERROR.value,
        "LocationServiceError": ErrorCode.LOCATION_SERVICE_ERROR.value,
        "ReservationServiceError": ErrorCode.RESERVATION_SERVICE_ERROR.value,
        "AuthServiceError": ErrorCode.AUTH_SERVICE_ERROR.value,
        
        # Excepciones de comunicación
        "ServiceUnavailableError": ErrorCode.SERVICE_UNAVAILABLE.value,
        "TimeoutError": ErrorCode.TIMEOUT_ERROR.value,
        "NetworkError": ErrorCode.NETWORK_ERROR.value,
    }
    
    return error_mapping.get(exception_name, ErrorCode.UNEXPECTED_ERROR.value)


 