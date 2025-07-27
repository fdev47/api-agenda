"""
Enumeración para días de la semana
"""
from enum import Enum


class DayOfWeek(Enum):
    """Días de la semana"""
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
    
    @classmethod
    def get_name(cls, day_number: int) -> str:
        """Obtener nombre del día por número"""
        names = {
            1: "Lunes",
            2: "Martes", 
            3: "Miércoles",
            4: "Jueves",
            5: "Viernes",
            6: "Sábado",
            7: "Domingo"
        }
        return names.get(day_number, "Desconocido") 