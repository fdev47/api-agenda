"""
Excepciones específicas para tipos de sector
"""
from .location_exceptions import LocationDomainException

class SectorTypeNotFoundException(LocationDomainException):
    def __init__(self, message: str, entity_id: int = None):
        super().__init__(
            message=message,
            error_code="SECTOR_TYPE_NOT_FOUND",
            entity_type="sector_type",
            entity_id=entity_id
        )

class SectorTypeAlreadyExistsException(LocationDomainException):
    def __init__(self, message: str, name: str = None, code: str = None):
        super().__init__(
            message=message,
            error_code="SECTOR_TYPE_ALREADY_EXISTS",
            entity_type="sector_type",
            additional_info={
                "name": name,
                "code": code
            }
        )

class SectorTypeValidationException(LocationDomainException):
    def __init__(self, message: str, field_errors: dict = None):
        super().__init__(
            message=message,
            error_code="SECTOR_TYPE_VALIDATION_ERROR",
            entity_type="sector_type",
            additional_info={
                "field_errors": field_errors or {}
            }
        ) 