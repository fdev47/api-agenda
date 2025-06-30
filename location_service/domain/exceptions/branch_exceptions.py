"""
Excepciones del dominio para sucursales
"""
from ...domain.exceptions.location_exceptions import LocationDomainException


class BranchNotFoundException(LocationDomainException):
    """Excepción cuando no se encuentra una sucursal"""
    
    def __init__(self, message: str, entity_id: int = None):
        super().__init__(message)
        self.entity_id = entity_id


class BranchAlreadyExistsException(LocationDomainException):
    """Excepción cuando ya existe una sucursal con el mismo código"""
    
    def __init__(self, message: str, code: str = None):
        super().__init__(message)
        self.code = code


class BranchValidationException(LocationDomainException):
    """Excepción cuando hay errores de validación en una sucursal"""
    
    def __init__(self, message: str, field_errors: dict = None):
        super().__init__(message)
        self.field_errors = field_errors or {} 