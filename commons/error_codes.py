"""
Códigos de error estandarizados para toda la aplicación
"""
from enum import Enum


class ErrorCode(Enum):
    """Códigos de error estandarizados"""
    
    # Errores de validación (400)
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_REQUEST = "INVALID_REQUEST"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    INVALID_FORMAT = "INVALID_FORMAT"
    
    # Errores de autenticación (401)
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    
    # Errores de autorización (403)
    FORBIDDEN = "FORBIDDEN"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    ACCESS_DENIED = "ACCESS_DENIED"
    
    # Errores de no encontrado (404)
    NOT_FOUND = "NOT_FOUND"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    
    # Errores de conflicto (409)
    CONFLICT = "CONFLICT"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"
    
    # Errores internos (500)
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    UNEXPECTED_ERROR = "INTERNAL_SERVER_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    
    # Errores de rate limiting (429)
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    
    # ===== RESERVATION SERVICE ERRORS =====
    
    # Errores de reserva (404)
    RESERVATION_NOT_FOUND = "RESERVATION_NOT_FOUND"
    
    # Errores de reserva (409)
    RESERVATION_ALREADY_EXISTS = "RESERVATION_ALREADY_EXISTS"
    RESERVATION_CONFLICT = "RESERVATION_CONFLICT"
    
    # Errores de reserva (400)
    RESERVATION_VALIDATION_ERROR = "RESERVATION_VALIDATION_ERROR"
    RESERVATION_STATUS_ERROR = "RESERVATION_STATUS_ERROR"
    INVALID_STATUS = "INVALID_STATUS"
    
    # ===== SCHEDULE SERVICE ERRORS =====
    
    # Errores de horario (404)
    SCHEDULE_NOT_FOUND = "SCHEDULE_NOT_FOUND"
    
    # Errores de horario (409)
    SCHEDULE_ALREADY_EXISTS = "SCHEDULE_ALREADY_EXISTS"
    SCHEDULE_OVERLAP = "SCHEDULE_OVERLAP"
    
    # Errores de horario (400)
    INVALID_SCHEDULE_TIME = "INVALID_SCHEDULE_TIME"
    INVALID_INTERVAL = "INVALID_INTERVAL"
    NO_SCHEDULE_FOR_DATE = "NO_SCHEDULE_FOR_DATE"
    SLOT_NOT_AVAILABLE = "SLOT_NOT_AVAILABLE"
    PAST_DATE = "PAST_DATE"
    INVALID_DAY_OF_WEEK = "INVALID_DAY_OF_WEEK"


def get_error_code_by_exception(exception: Exception) -> str:
    """
    Mapear excepciones a códigos de error específicos
    
    Args:
        exception: Excepción a mapear
        
    Returns:
        str: Código de error correspondiente
    """
    exception_name = exception.__class__.__name__
    
    # Mapeo de excepciones específicas
    exception_mapping = {
        'ValidationError': ErrorCode.VALIDATION_ERROR.value,
        'ValueError': ErrorCode.VALIDATION_ERROR.value,
        'TypeError': ErrorCode.VALIDATION_ERROR.value,
        'KeyError': ErrorCode.VALIDATION_ERROR.value,
        'AttributeError': ErrorCode.VALIDATION_ERROR.value,
        
        'UnauthorizedException': ErrorCode.UNAUTHORIZED.value,
        'AuthenticationError': ErrorCode.UNAUTHORIZED.value,
        'TokenExpiredError': ErrorCode.TOKEN_EXPIRED.value,
        
        'ForbiddenException': ErrorCode.FORBIDDEN.value,
        'PermissionDeniedError': ErrorCode.FORBIDDEN.value,
        
        'NotFoundException': ErrorCode.NOT_FOUND.value,
        'UserNotFoundException': ErrorCode.USER_NOT_FOUND.value,
        'ResourceNotFoundException': ErrorCode.RESOURCE_NOT_FOUND.value,
        
        'ConflictException': ErrorCode.CONFLICT.value,
        'UserAlreadyExistsException': ErrorCode.USER_ALREADY_EXISTS.value,
        'ResourceAlreadyExistsException': ErrorCode.RESOURCE_ALREADY_EXISTS.value,
        
        'DatabaseError': ErrorCode.DATABASE_ERROR.value,
        'ConnectionError': ErrorCode.EXTERNAL_SERVICE_ERROR.value,
        'TimeoutError': ErrorCode.EXTERNAL_SERVICE_ERROR.value,
        
        # ===== RESERVATION SERVICE EXCEPTIONS =====
        'ReservationNotFoundException': ErrorCode.RESERVATION_NOT_FOUND.value,
        'ReservationAlreadyExistsException': ErrorCode.RESERVATION_ALREADY_EXISTS.value,
        'ReservationConflictException': ErrorCode.RESERVATION_CONFLICT.value,
        'ReservationValidationException': ErrorCode.RESERVATION_VALIDATION_ERROR.value,
        'ReservationStatusException': ErrorCode.RESERVATION_STATUS_ERROR.value,
        
        # ===== SCHEDULE SERVICE EXCEPTIONS =====
        'ScheduleNotFoundException': ErrorCode.SCHEDULE_NOT_FOUND.value,
        'ScheduleAlreadyExistsException': ErrorCode.SCHEDULE_ALREADY_EXISTS.value,
        'ScheduleOverlapException': ErrorCode.SCHEDULE_OVERLAP.value,
        'InvalidScheduleTimeException': ErrorCode.INVALID_SCHEDULE_TIME.value,
        'InvalidIntervalException': ErrorCode.INVALID_INTERVAL.value,
        'NoScheduleForDateException': ErrorCode.NO_SCHEDULE_FOR_DATE.value,
        'SlotNotAvailableException': ErrorCode.SLOT_NOT_AVAILABLE.value,
        'PastDateException': ErrorCode.PAST_DATE.value,
    }
    
    return exception_mapping.get(exception_name, ErrorCode.INTERNAL_SERVER_ERROR.value)


 