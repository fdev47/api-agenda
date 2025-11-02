"""
Modelo de base de datos para la tabla principal de reservas (main_reservations)
"""
import logging
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from .base import Base

logger = logging.getLogger(__name__)


# Importar la entidad de dominio de forma lazy para evitar imports circulares
if TYPE_CHECKING:
    from ...domain.entities.main_reservation import MainReservation


class MainReservationModel(Base):
    """Modelo de base de datos para main_reservations"""

    __tablename__ = "main_reservations"

    # Clave primaria
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Campos requeridos
    sector_id = Column(Integer, nullable=False, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False, index=True)
    ramp_id = Column(Integer, nullable=False, index=True)
    sector_data = Column(JSON, nullable=False)

    # Campos de auditoría
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Horario de la reserva
    reservation_date = Column(DateTime, nullable=False, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)

    # Relaciones
    reservation = relationship("ReservationModel", backref="main_reservations")

    def to_domain(self) -> 'MainReservation':
        """Convierte el modelo de BD a entidad de dominio"""
        try:
            from ...domain.entities.main_reservation import MainReservation
            from ...domain.entities.sector_data import SectorData
            
            # Convertir datos JSON a objeto de dominio
            sector_data = SectorData(**self.sector_data)
            
            return MainReservation(
                id=self.id,
                sector_id=self.sector_id,
                reservation_id=self.reservation_id,
                ramp_id=self.ramp_id,
                sector_data=sector_data,
                reservation_date=self.reservation_date,
                start_time=self.start_time,
                end_time=self.end_time,
                created_at=self.created_at,
                updated_at=self.updated_at
            )
        except Exception as e:
            logger.error(f"❌ Error en MainReservationModel.to_domain(): {str(e)}", exc_info=True)
            raise

    @classmethod
    def from_domain(cls, main_reservation: 'MainReservation') -> 'MainReservationModel':
        """Convierte la entidad de dominio a modelo de BD"""
        try:
            # Convertir objeto de dominio a JSON
            sector_data = {
                "sector_id": main_reservation.sector_data.sector_id,
                "name": main_reservation.sector_data.name,
                "sector_type_id": main_reservation.sector_data.sector_type_id,
                "sector_type_name": main_reservation.sector_data.sector_type_name,
                "measurement_unit_id": main_reservation.sector_data.measurement_unit_id,
                "measurement_unit_name": main_reservation.sector_data.measurement_unit_name,
                "description": main_reservation.sector_data.description,
                "capacity": main_reservation.sector_data.capacity,
                "pallet_count": main_reservation.sector_data.pallet_count,
                "granel_count": main_reservation.sector_data.granel_count,
                "boxes_count": main_reservation.sector_data.boxes_count
            }
            
            return cls(
                id=main_reservation.id,
                sector_id=main_reservation.sector_id,
                reservation_id=main_reservation.reservation_id,
                ramp_id=main_reservation.ramp_id,
                sector_data=sector_data,
                reservation_date=main_reservation.reservation_date,
                start_time=main_reservation.start_time,
                end_time=main_reservation.end_time,
                created_at=main_reservation.created_at,
                updated_at=main_reservation.updated_at
            )
        except Exception as e:
            logger.error(f"❌ Error en MainReservationModel.from_domain(): {str(e)}", exc_info=True)
            raise

    def __repr__(self):
        return (
            f"<MainReservationModel(id={self.id}, reservation_id={self.reservation_id}, "
            f"sector_id={self.sector_id}, ramp_id={self.ramp_id})>"
        )


