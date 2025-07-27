"""
Interfaz para el repositorio de reservas
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from datetime import datetime
from ..entities.reservation import Reservation
from ..dto.requests.reservation_filter_request import ReservationFilterRequest


class ReservationRepository(ABC):
    """Interfaz del repositorio para reservas"""
    
    @abstractmethod
    async def create(self, reservation: Reservation) -> Reservation:
        """Crear una nueva reserva"""
        pass
    
    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """Obtener una reserva por ID"""
        pass
    
    @abstractmethod
    async def list(self, filter_request: ReservationFilterRequest) -> Tuple[List[Reservation], int]:
        """Listar reservas con filtros y paginación"""
        pass
    
    @abstractmethod
    async def update(self, reservation: Reservation) -> Reservation:
        """Actualizar una reserva"""
        pass
    
    @abstractmethod
    async def delete(self, reservation_id: int) -> bool:
        """Eliminar una reserva"""
        pass
    
    @abstractmethod
    async def exists_conflict(self, branch_id: int, sector_id: int, start_time: datetime, end_time: datetime, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un conflicto de horario"""
        pass
    
    @abstractmethod
    async def check_conflicts(self, branch_id: int, sector_id: int, start_time: datetime, end_time: datetime, exclude_reservation_id: Optional[int] = None) -> List[Reservation]:
        """Verificar conflictos de horario y retornar las reservas que causan conflicto"""
        pass
    
    @abstractmethod
    async def get_conflicting_reservation(self, branch_id: int, sector_id: int, start_time: datetime, end_time: datetime, exclude_id: Optional[int] = None) -> Optional[Reservation]:
        """Obtener la reserva que causa conflicto de horario"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: int, limit: int = 10) -> List[Reservation]:
        """Obtener reservas por usuario"""
        pass
    
    @abstractmethod
    async def get_by_customer_id(self, customer_id: int, limit: int = 10) -> List[Reservation]:
        """Obtener reservas por cliente"""
        pass
    
    @abstractmethod
    async def get_by_branch_id(self, branch_id: int, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> List[Reservation]:
        """Obtener reservas por sucursal"""
        pass
    
    @abstractmethod
    async def get_by_sector_id(self, sector_id: int, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> List[Reservation]:
        """Obtener reservas por sector"""
        pass
    
    @abstractmethod
    async def get_active_reservations(self, branch_id: Optional[int] = None, sector_id: Optional[int] = None) -> List[Reservation]:
        """Obtener reservas activas (pendientes o confirmadas)"""
        pass
    
    @abstractmethod
    async def update_status(self, reservation_id: int, status: str) -> bool:
        """Actualizar solo el estado de una reserva"""
        pass 