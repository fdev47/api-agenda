"""
Excepciones del dominio para locales
"""
from ...domain.exceptions.location_exceptions import LocationDomainException


class LocalNotFoundException(LocationDomainException):
    """Excepción cuando no se encuentra un local"""
    
    def __init__(self, message: str, entity_id: int = None):
        super().__init__(message)
        self.entity_id = entity_id


class LocalAlreadyExistsException(LocationDomainException):
    """Excepción cuando ya existe un local con el mismo código"""
    
    def __init__(self, message: str, code: str = None):
        super().__init__(message)
        self.code = code


class LocalValidationException(LocationDomainException):
    """Excepción cuando hay errores de validación en un local"""
    
    def __init__(self, message: str, field_errors: dict = None):
        super().__init__(message)
        self.field_errors = field_errors or {} 