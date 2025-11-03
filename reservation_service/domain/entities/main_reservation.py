"""
Entidad para la reserva principal (main_reservation)
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from .sector_data import SectorData


@dataclass
class MainReservation:
    """Entidad MainReservation - representa una reserva principal con datos simplificados"""
    
    # IDs de referencia
    sector_id: int
    reservation_id: int
    
    # Datos del sector (completos, no solo ID - incluye ramp_id y ramp_name)
    sector_data: SectorData
    
    # Horario de la reserva
    reservation_date: datetime
    start_time: datetime
    end_time: datetime
    
    # Identificación básica
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones después de la inicialización"""
        if not self.sector_data:
            raise ValueError("Los datos del sector son obligatorios")
        
        if not self.reservation_date:
            raise ValueError("La fecha de reserva es obligatoria")
        
        if not self.start_time or not self.end_time:
            raise ValueError("El horario de inicio y fin es obligatorio")
        
        if self.start_time >= self.end_time:
            raise ValueError("El horario de inicio debe ser anterior al de fin")
        
        if self.sector_id <= 0:
            raise ValueError("El sector_id debe ser mayor a 0")
        
        if self.reservation_id <= 0:
            raise ValueError("El reservation_id debe ser mayor a 0")
        
        # Asignar timestamps si no están definidos
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()

    def __repr__(self):
        return (
            f"<MainReservation(id={self.id}, reservation_id={self.reservation_id}, "
            f"sector_id={self.sector_id}, ramp_id={self.sector_data.ramp_id if self.sector_data else 'N/A'})>"
        )

