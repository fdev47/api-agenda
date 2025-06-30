"""
Excepciones específicas para rampas
"""
from .location_exceptions import LocationDomainException


class RampNotFoundException(LocationDomainException):
    """Excepción lanzada cuando no se encuentra una rampa"""
    
    def __init__(self, message: str, entity_id: int = None):
        super().__init__(
            message=message,
            error_code="RAMP_NOT_FOUND",
            entity_type="ramp",
            entity_id=entity_id
        )


class RampAlreadyExistsException(LocationDomainException):
    """Excepción lanzada cuando ya existe una rampa con el mismo nombre en la misma sucursal"""
    
    def __init__(self, message: str, name: str = None, branch_id: int = None):
        super().__init__(
            message=message,
            error_code="RAMP_ALREADY_EXISTS",
            entity_type="ramp",
            additional_info={
                "name": name,
                "branch_id": branch_id
            }
        )


class RampValidationException(LocationDomainException):
    """Excepción lanzada cuando hay errores de validación en una rampa"""
    
    def __init__(self, message: str, field_errors: dict = None):
        super().__init__(
            message=message,
            error_code="RAMP_VALIDATION_ERROR",
            entity_type="ramp",
            additional_info={
                "field_errors": field_errors or {}
            }
        ) 