from datetime import datetime, time
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


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


@dataclass
class BranchSchedule:
    """Horario configurado para una sucursal"""
    id: Optional[int] = None
    branch_id: int = None
    day_of_week: DayOfWeek = None
    start_time: time = None
    end_time: time = None
    interval_minutes: int = 60  # Intervalo por defecto 1 hora
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if not self.branch_id or self.branch_id <= 0:
            raise ValueError("El ID de la sucursal es obligatorio")
        
        if not self.day_of_week:
            raise ValueError("El día de la semana es obligatorio")
        
        if not self.start_time or not self.end_time:
            raise ValueError("Los horarios de inicio y fin son obligatorios")
        
        if self.start_time >= self.end_time:
            raise ValueError("El horario de inicio debe ser anterior al de fin")
        
        if self.interval_minutes <= 0:
            raise ValueError("El intervalo debe ser mayor a 0")
        
        if self.interval_minutes > self.duration_minutes():
            raise ValueError("El intervalo no puede ser mayor que la duración total")
        
        # Asignar timestamps si no están definidos
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()
    
    def duration_minutes(self) -> int:
        """Obtener duración total en minutos"""
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute
        return end_minutes - start_minutes
    
    def duration_hours(self) -> float:
        """Obtener duración total en horas"""
        return self.duration_minutes() / 60.0
    
    def generate_time_slots(self) -> List[TimeSlot]:
        """Generar slots de tiempo dinámicamente"""
        slots = []
        current_time = self.start_time
        
        while current_time < self.end_time:
            # Calcular tiempo de fin del slot
            current_minutes = current_time.hour * 60 + current_time.minute
            end_minutes = current_minutes + self.interval_minutes
            
            # Convertir de vuelta a time
            end_time = time(hour=end_minutes // 60, minute=end_minutes % 60)
            
            # Asegurar que no exceda el horario de fin
            if end_time > self.end_time:
                end_time = self.end_time
            
            # Crear slot
            slot = TimeSlot(
                start_time=current_time,
                end_time=end_time
            )
            slots.append(slot)
            
            # Avanzar al siguiente slot
            current_time = end_time
        
        return slots
    
    def get_day_name(self) -> str:
        """Obtener nombre del día"""
        return DayOfWeek.get_name(self.day_of_week.value)
    
    def is_same_day(self, other: 'BranchSchedule') -> bool:
        """Verificar si es el mismo día"""
        return self.day_of_week == other.day_of_week
    
    def overlaps_with(self, other: 'BranchSchedule') -> bool:
        """Verificar si hay solapamiento con otro horario"""
        if not self.is_same_day(other):
            return False
        
        return not (self.end_time <= other.start_time or other.end_time <= self.start_time)


@dataclass
class AvailableSlotsResponse:
    """Respuesta con slots disponibles para una fecha"""
    branch_id: int
    branch_name: str
    date: datetime
    day_of_week: int
    day_name: str
    slots: List[TimeSlot]
    total_slots: int
    available_slots: int
    
    def __post_init__(self):
        """Calcular estadísticas"""
        self.total_slots = len(self.slots)
        self.available_slots = len([slot for slot in self.slots if slot.is_available]) 