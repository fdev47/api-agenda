"""
Entidad para slots de tiempo
"""
from datetime import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class TimeSlot:
    """Slot de tiempo disponible"""
    start_time: time
    end_time: time
    is_available: bool = True
    reservation_id: Optional[int] = None
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if self.start_time >= self.end_time:
            raise ValueError("El tiempo de inicio debe ser anterior al de fin")
    
    def overlaps_with(self, other: 'TimeSlot') -> bool:
        """Verificar si hay solapamiento con otro slot"""
        return not (self.end_time <= other.start_time or other.end_time <= self.start_time)
    
    def contains(self, check_time: time) -> bool:
        """Verificar si un tiempo está dentro del slot"""
        return self.start_time <= check_time < self.end_time
    
    def duration_minutes(self) -> int:
        """Obtener duración en minutos"""
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute
        return end_minutes - start_minutes
    
    def duration_hours(self) -> float:
        """Obtener duración en horas"""
        return self.duration_minutes() / 60.0 