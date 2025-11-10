"""
Interfaz del repositorio para horarios de rampas
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.ramp_schedule import RampSchedule
from ..dto.requests.ramp_schedule_requests import RampScheduleFilterRequest


class RampScheduleRepository(ABC):
    """Interfaz del repositorio para horarios de rampas"""
    
    @abstractmethod
    async def create(self, schedule: RampSchedule) -> RampSchedule:
        """Crear un nuevo horario"""
        pass
    
    @abstractmethod
    async def get_by_id(self, schedule_id: int) -> Optional[RampSchedule]:
        """Obtener un horario por ID"""
        pass
    
    @abstractmethod
    async def get_by_ramp_id(self, ramp_id: int) -> List[RampSchedule]:
        """Obtener todos los horarios de una rampa"""
        pass
    
    @abstractmethod
    async def get_by_ramp_and_day(self, ramp_id: int, day_of_week: int) -> List[RampSchedule]:
        """Obtener horarios de una rampa para un día específico"""
        pass
    
    @abstractmethod
    async def list(self, filter_request: RampScheduleFilterRequest) -> tuple[List[RampSchedule], int]:
        """Listar horarios con filtros y paginación"""
        pass
    
    @abstractmethod
    async def update(self, schedule: RampSchedule) -> RampSchedule:
        """Actualizar un horario"""
        pass
    
    @abstractmethod
    async def delete(self, schedule_id: int) -> bool:
        """Eliminar un horario"""
        pass

