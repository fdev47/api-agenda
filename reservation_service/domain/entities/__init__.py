# Entidades de reserva
from .reservation_status import ReservationStatus
from .order_number import OrderNumber
from .customer_data import CustomerData
from .branch_data import BranchData
from .sector_data import SectorData
from .reservation import Reservation
from .main_reservation import MainReservation

# Entidades de schedule
from .day_of_week import DayOfWeek
from .time_slot import TimeSlot
from .branch_schedule import BranchSchedule
from .available_slots_response import AvailableSlotsResponse

__all__ = [
    # Reserva
    "Reservation",
    "MainReservation",
    "ReservationStatus",
    "OrderNumber",
    "CustomerData",
    "BranchData",
    "SectorData",
    # Schedule
    "DayOfWeek",
    "TimeSlot",
    "BranchSchedule",
    "AvailableSlotsResponse"
]
