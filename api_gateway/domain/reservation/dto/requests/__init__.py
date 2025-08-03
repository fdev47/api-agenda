"""
Reservation request DTOs for API Gateway
"""
from .available_ramp_request import AvailableRampRequest
from .create_reservation_request import CreateReservationRequest
from .update_reservation_request import UpdateReservationRequest
from .reservation_filter_request import ReservationFilterRequest
from .order_number_request import OrderNumberRequest
from .customer_data_request import CustomerDataRequest
from .sector_data_request import SectorDataRequest
from .branch_data_request import BranchDataRequest

__all__ = [
    "AvailableRampRequest",
    "CreateReservationRequest",
    "UpdateReservationRequest",
    "ReservationFilterRequest",
    "OrderNumberRequest",
    "CustomerDataRequest",
    "SectorDataRequest",
    "BranchDataRequest"
] 