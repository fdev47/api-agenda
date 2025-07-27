"""
Entidad para respuesta de slots disponibles
"""
from datetime import datetime
from typing import List
from dataclasses import dataclass

from .time_slot import TimeSlot


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