"""
Enumeración para los estados de reserva
"""
from enum import Enum


class ReservationStatus(Enum):
    """Estados de una reserva"""
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    RESCHEDULING_REQUIRED = "RESCHEDULING_REQUIRED"  # Nuevo estado para reagendamiento 