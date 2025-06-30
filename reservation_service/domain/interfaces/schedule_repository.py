from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date, datetime

from ..entities.schedule import BranchSchedule, DayOfWeek, TimeSlot
from ..entities.reservation import Reservation


class ScheduleRepository(ABC):
    """Interfaz para el repositorio de horarios de sucursales"""
    
    @abstractmethod
    async def create(self, schedule: BranchSchedule) -> BranchSchedule:
        """Crear un nuevo horario de sucursal"""
        pass
    
    @abstractmethod
    async def get_by_id(self, schedule_id: int) -> Optional[BranchSchedule]:
        """Obtener un horario por ID"""
        pass
    
    @abstractmethod
    async def get_by_branch_and_day(self, branch_id: int, day_of_week: DayOfWeek) -> Optional[BranchSchedule]:
        """Obtener horario de una sucursal para un día específico"""
        pass
    
    @abstractmethod
    async def list_by_branch(self, branch_id: int, day_of_week: Optional[DayOfWeek] = None, 
                           is_active: Optional[bool] = None) -> List[BranchSchedule]:
        """Listar horarios de una sucursal con filtros opcionales"""
        pass
    
    @abstractmethod
    async def update(self, schedule_id: int, schedule_data: dict) -> Optional[BranchSchedule]:
        """Actualizar un horario existente"""
        pass
    
    @abstractmethod
    async def delete(self, schedule_id: int) -> bool:
        """Eliminar un horario"""
        pass
    
    @abstractmethod
    async def exists_by_branch_and_day(self, branch_id: int, day_of_week: DayOfWeek, 
                                     exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un horario para una sucursal y día"""
        pass
    
    @abstractmethod
    async def get_available_slots(self, branch_id: int, target_date: date) -> List[TimeSlot]:
        """Obtener slots disponibles para una fecha específica"""
        pass
    
    @abstractmethod
    async def check_slot_availability(self, branch_id: int, target_date: date, 
                                    start_time: str, end_time: str) -> bool:
        """Verificar si un slot específico está disponible"""
        pass
    
    @abstractmethod
    async def get_reservations_for_date(self, branch_id: int, target_date: date) -> List[Reservation]:
        """Obtener reservas existentes para una fecha específica"""
        pass 