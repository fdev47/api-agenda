"""
Interfaz para el repositorio de main_reservations
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from datetime import datetime

from ..entities.main_reservation import MainReservation


class MainReservationRepository(ABC):
    """Interfaz del repositorio para main_reservations"""
    
    @abstractmethod
    async def create(self, main_reservation: MainReservation) -> MainReservation:
        """Crear una nueva main_reservation"""
        pass
    
    @abstractmethod
    async def get_by_id(self, main_reservation_id: int) -> Optional[MainReservation]:
        """Obtener una main_reservation por ID"""
        pass
    
    @abstractmethod
    async def list(
        self,
        sector_id: Optional[int] = None,
        reservation_id: Optional[int] = None,
        reservation_date: Optional[datetime] = None,
        start_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[MainReservation], int]:
        """
        Listar main_reservations con filtros
        
        Args:
            sector_id: Filtrar por sector_id
            reservation_id: Filtrar por reservation_id
            reservation_date: Filtrar por fecha de reserva
            start_time: Filtrar por hora de inicio
            skip: Número de registros a saltar (paginación)
            limit: Número máximo de registros a retornar
            
        Returns:
            Tuple[List[MainReservation], int]: Lista de reservas y total de registros
        """
        pass
    
    @abstractmethod
    async def update(self, main_reservation: MainReservation) -> MainReservation:
        """Actualizar una main_reservation"""
        pass
    
    @abstractmethod
    async def delete(self, main_reservation_id: int) -> bool:
        """
        Eliminar una main_reservation por ID
        
        Args:
            main_reservation_id: ID de la main_reservation a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        pass

