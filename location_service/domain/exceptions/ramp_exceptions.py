"""
Excepciones específicas para rampas
"""
from ..exceptions import LocationDomainException


class RampNotFoundException(LocationDomainException):
    """Excepción cuando no se encuentra una rampa"""
    
    def __init__(self, message: str, entity_id: int = None):
        super().__init__(message, "RAMP_NOT_FOUND", "ramp", entity_id)


class RampAlreadyExistsException(LocationDomainException):
    """Excepción cuando ya existe una rampa con el mismo nombre en la misma sucursal"""
    
    def __init__(self, message: str, name: str = None, branch_id: int = None):
        super().__init__(message, "RAMP_ALREADY_EXISTS", "ramp")
        self.name = name
        self.branch_id = branch_id


class RampValidationException(LocationDomainException):
    """Excepción cuando hay errores de validación en una rampa"""
    
    def __init__(self, message: str, field_errors: dict = None):
        super().__init__(message, "RAMP_VALIDATION_ERROR", "ramp")
        self.field_errors = field_errors or {}


 