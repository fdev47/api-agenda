"""
Entidad RampSchedule del dominio de ubicaciones
"""
from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional
from .day_of_week import DayOfWeek


@dataclass
class RampSchedule:
    """Entidad RampSchedule - representa un horario/turno de una rampa"""
    
    id: int
    ramp_id: int
    day_of_week: int  # 1=Lunes, 7=Domingo
    name: str  # "Turno 1", "Horario descarga", etc.
    start_time: time
    end_time: time
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if self.ramp_id <= 0:
            raise ValueError("El ID de la rampa debe ser mayor a 0")
        
        if not (1 <= self.day_of_week <= 7):
            raise ValueError("El día de la semana debe estar entre 1 (Lunes) y 7 (Domingo)")
        
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del horario no puede estar vacío")
        
        if len(self.name) > 100:
            raise ValueError("El nombre del horario no puede exceder 100 caracteres")
        
        if self.start_time >= self.end_time:
            raise ValueError("La hora de inicio debe ser menor a la hora de fin")
    
    def activate(self) -> None:
        """Activar el horario"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Desactivar el horario"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def update_times(self, start_time: time, end_time: time) -> None:
        """Actualizar las horas del turno"""
        if start_time >= end_time:
            raise ValueError("La hora de inicio debe ser menor a la hora de fin")
        
        self.start_time = start_time
        self.end_time = end_time
        self.updated_at = datetime.utcnow()
    
    def update_name(self, new_name: str) -> None:
        """Actualizar el nombre del horario"""
        if not new_name or not new_name.strip():
            raise ValueError("El nombre del horario no puede estar vacío")
        
        if len(new_name) > 100:
            raise ValueError("El nombre del horario no puede exceder 100 caracteres")
        
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow()
    
    def get_day_name(self) -> str:
        """Obtener el nombre del día en español"""
        return DayOfWeek.get_name(self.day_of_week)

