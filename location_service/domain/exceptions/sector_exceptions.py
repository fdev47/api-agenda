"""
Excepciones específicas para sectores
"""
from .location_exceptions import LocationDomainException


class SectorNotFoundException(LocationDomainException):
    """Excepción lanzada cuando no se encuentra un sector"""
    
    def __init__(self, message: str, entity_id: int = None):
        super().__init__(
            message=message,
            error_code="SECTOR_NOT_FOUND",
            entity_type="sector",
            entity_id=entity_id
        )


class SectorAlreadyExistsException(LocationDomainException):
    """Excepción lanzada cuando ya existe un sector con el mismo nombre en la misma sucursal"""
    
    def __init__(self, message: str, name: str = None, branch_id: int = None):
        super().__init__(
            message=message,
            error_code="SECTOR_ALREADY_EXISTS",
            entity_type="sector",
            additional_info={
                "name": name,
                "branch_id": branch_id
            }
        )


class SectorValidationException(LocationDomainException):
    """Excepción lanzada cuando hay errores de validación en un sector"""
    
    def __init__(self, message: str, field_errors: dict = None):
        super().__init__(
            message=message,
            error_code="SECTOR_VALIDATION_ERROR",
            entity_type="sector",
            additional_info={
                "field_errors": field_errors or {}
            }
        ) 