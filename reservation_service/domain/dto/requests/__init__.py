# Reservation Service request DTOs

# Data DTOs
from .order_number_request import OrderNumberRequest
from .customer_data_request import CustomerDataRequest
from .branch_data_request import BranchDataRequest
from .sector_data_request import SectorDataRequest

# Main reservation DTOs
from .create_reservation_request import CreateReservationRequest
from .update_reservation_request import UpdateReservationRequest
from .reservation_filter_request import ReservationFilterRequest

# Schedule DTOs (from existing file)
from .schedule_requests import (
    CreateBranchScheduleRequest,
    UpdateBranchScheduleRequest,
    GetAvailableSlotsRequest,
    GetBranchSchedulesRequest
)

__all__ = [
    # Data DTOs
    "OrderNumberRequest",
    "CustomerDataRequest",
    "BranchDataRequest",
    "SectorDataRequest",
    # Main reservation DTOs
    "CreateReservationRequest",
    "UpdateReservationRequest", 
    "ReservationFilterRequest",
    # Schedule DTOs
    "CreateBranchScheduleRequest",
    "UpdateBranchScheduleRequest",
    "GetAvailableSlotsRequest",
    "GetBranchSchedulesRequest"
]
