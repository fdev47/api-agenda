class ScheduleNotFoundException(Exception):
    """Excepción cuando no se encuentra un horario"""
    
    def __init__(self, schedule_id: int = None, branch_id: int = None, day_of_week: str = None):
        if schedule_id:
            message = f"Horario con ID {schedule_id} no encontrado"
        elif branch_id and day_of_week:
            message = f"Horario para sucursal {branch_id} en {day_of_week} no encontrado"
        else:
            message = "Horario no encontrado"
        
        self.message = message
        self.error_code = "SCHEDULE_NOT_FOUND"
        super().__init__(self.message)


class ScheduleAlreadyExistsException(Exception):
    """Excepción cuando ya existe un horario para la misma sucursal y día"""
    
    def __init__(self, branch_id: int, day_of_week: str):
        message = f"Ya existe un horario para la sucursal {branch_id} en {day_of_week}"
        self.message = message
        self.error_code = "SCHEDULE_ALREADY_EXISTS"
        super().__init__(self.message)


class ScheduleOverlapException(Exception):
    """Excepción cuando hay solapamiento de horarios"""
    
    def __init__(self, branch_id: int, day_of_week: str, start_time: str, end_time: str):
        message = f"El horario {start_time}-{end_time} para {day_of_week} se solapa con un horario existente en la sucursal {branch_id}"
        self.message = message
        self.error_code = "SCHEDULE_OVERLAP"
        super().__init__(self.message)


class InvalidScheduleTimeException(Exception):
    """Excepción cuando los horarios son inválidos"""
    
    def __init__(self, start_time: str, end_time: str):
        message = f"Horario inválido: {start_time}-{end_time}. El tiempo de inicio debe ser anterior al de fin"
        self.message = message
        self.error_code = "INVALID_SCHEDULE_TIME"
        super().__init__(self.message)


class InvalidIntervalException(Exception):
    """Excepción cuando el intervalo es inválido"""
    
    def __init__(self, interval_minutes: int, duration_minutes: int):
        message = f"Intervalo inválido: {interval_minutes} minutos. No puede ser mayor que la duración total ({duration_minutes} minutos)"
        self.message = message
        self.error_code = "INVALID_INTERVAL"
        super().__init__(self.message)


class NoScheduleForDateException(Exception):
    """Excepción cuando no hay horario configurado para una fecha"""
    
    def __init__(self, branch_id: int, date: str, day_of_week: str):
        message = f"No hay horario configurado para la sucursal {branch_id} en {day_of_week} ({date})"
        self.message = message
        self.error_code = "NO_SCHEDULE_FOR_DATE"
        super().__init__(self.message)


class SlotNotAvailableException(Exception):
    """Excepción cuando un slot no está disponible"""
    
    def __init__(self, branch_id: int, date: str, start_time: str, end_time: str):
        message = f"El slot {start_time}-{end_time} del {date} no está disponible en la sucursal {branch_id}"
        self.message = message
        self.error_code = "SLOT_NOT_AVAILABLE"
        super().__init__(self.message)


class PastDateException(Exception):
    """Excepción cuando se intenta consultar una fecha pasada"""
    
    def __init__(self, date: str):
        message = f"No se puede consultar disponibilidad para fechas pasadas: {date}"
        self.message = message
        self.error_code = "PAST_DATE"
        super().__init__(self.message) 