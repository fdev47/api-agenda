"""
Excepciones específicas para reservas
"""
from commons.error_codes import ErrorCode


class ReservationNotFoundException(Exception):
    """Excepción lanzada cuando no se encuentra una reserva"""
    
    def __init__(self, message: str, reservation_id: int = None):
        self.message = message
        self.reservation_id = reservation_id
        self.error_code = ErrorCode.RESERVATION_NOT_FOUND.value
        super().__init__(self.message)


class ReservationAlreadyExistsException(Exception):
    """Excepción lanzada cuando ya existe una reserva en el mismo horario"""
    
    def __init__(self, message: str, branch_id: int = None, sector_id: int = None, start_time=None, end_time=None):
        self.message = message
        self.branch_id = branch_id
        self.sector_id = sector_id
        self.start_time = start_time
        self.end_time = end_time
        self.error_code = ErrorCode.RESERVATION_ALREADY_EXISTS.value
        super().__init__(self.message)


class ReservationValidationException(Exception):
    """Excepción lanzada cuando hay errores de validación en una reserva"""
    
    def __init__(self, message: str, field_errors: dict = None):
        self.message = message
        self.field_errors = field_errors or {}
        self.error_code = ErrorCode.RESERVATION_VALIDATION_ERROR.value
        super().__init__(self.message)


class ReservationConflictException(Exception):
    """Excepción lanzada cuando hay conflictos de horario en una reserva"""
    
    def __init__(self, message: str, conflicting_reservation_id: int = None, branch_id: int = None, sector_id: int = None):
        self.message = message
        self.conflicting_reservation_id = conflicting_reservation_id
        self.branch_id = branch_id
        self.sector_id = sector_id
        self.error_code = ErrorCode.RESERVATION_CONFLICT.value
        super().__init__(self.message)


class ReservationStatusException(Exception):
    """Excepción lanzada cuando hay errores relacionados con el estado de la reserva"""
    
    def __init__(self, message: str, current_status: str = None, required_status: str = None):
        self.message = message
        self.current_status = current_status
        self.required_status = required_status
        self.error_code = ErrorCode.RESERVATION_STATUS_ERROR.value
        super().__init__(self.message) 