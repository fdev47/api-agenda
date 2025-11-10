"""
Excepciones personalizadas para horarios de rampas
"""


class RampScheduleNotFoundException(Exception):
    """Excepción lanzada cuando no se encuentra un horario de rampa"""
    
    def __init__(self, schedule_id: int):
        self.schedule_id = schedule_id
        super().__init__(f"Horario de rampa con ID {schedule_id} no encontrado")


class RampScheduleAlreadyExistsException(Exception):
    """Excepción lanzada cuando ya existe un horario con los mismos datos"""
    
    def __init__(self, message: str, ramp_id: int, day_of_week: int, name: str):
        self.ramp_id = ramp_id
        self.day_of_week = day_of_week
        self.name = name
        super().__init__(message)


class InvalidTimeRangeException(Exception):
    """Excepción lanzada cuando el rango de tiempo es inválido"""
    
    def __init__(self, message: str):
        super().__init__(message)

