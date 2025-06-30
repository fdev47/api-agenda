"""
Excepciones del dominio para ubicaciones
"""
from typing import Optional


class LocationDomainException(Exception):
    """Excepción base para errores del dominio de ubicaciones"""
    
    def __init__(self, message: str, error_code: str = None, entity_type: str = None, entity_id: int = None):
        self.message = message
        self.error_code = error_code
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(self.message)


class CountryNotFoundException(LocationDomainException):
    """Excepción cuando no se encuentra un país"""
    
    def __init__(self, message: str, entity_id: int = None):
        super().__init__(message, "COUNTRY_NOT_FOUND", "country", entity_id)


class CountryAlreadyExistsException(LocationDomainException):
    """Excepción cuando ya existe un país con el mismo código"""
    
    def __init__(self, message: str, code: str = None):
        super().__init__(message, "COUNTRY_ALREADY_EXISTS", "country")
        self.code = code


class StateNotFoundException(LocationDomainException):
    """Excepción cuando no se encuentra un estado"""
    
    def __init__(self, message: str, entity_id: int = None):
        super().__init__(message, "STATE_NOT_FOUND", "state", entity_id)


class StateAlreadyExistsException(LocationDomainException):
    """Excepción cuando ya existe un estado con el mismo código"""
    
    def __init__(self, message: str, code: str = None):
        super().__init__(message, "STATE_ALREADY_EXISTS", "state")
        self.code = code


class CityNotFoundException(LocationDomainException):
    """Excepción cuando no se encuentra una ciudad"""
    
    def __init__(self, message: str, entity_id: int = None):
        super().__init__(message, "CITY_NOT_FOUND", "city", entity_id)


class CityAlreadyExistsException(LocationDomainException):
    """Excepción cuando ya existe una ciudad con el mismo código"""
    
    def __init__(self, message: str, code: str = None):
        super().__init__(message, "CITY_ALREADY_EXISTS", "city")
        self.code = code


class LocationValidationException(LocationDomainException):
    """Excepción cuando hay errores de validación en ubicaciones"""
    
    def __init__(self, message: str, field_errors: dict = None, entity_type: str = None):
        super().__init__(message, "LOCATION_VALIDATION_ERROR", entity_type)
        self.field_errors = field_errors or {} 