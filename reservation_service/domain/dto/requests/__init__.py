# Reservation Service request DTOs

from .reservation_requests import (
    CreateReservationRequest,
    UpdateReservationRequest,
    ReservationFilterRequest,
    OrderNumberRequest,
    CustomerDataRequest,
    BranchDataRequest,
    SectorDataRequest
)
from .schedule_requests import (
    CreateBranchScheduleRequest,
    UpdateBranchScheduleRequest,
    GetAvailableSlotsRequest,
    GetBranchSchedulesRequest
)

__all__ = [
    "CreateReservationRequest",
    "UpdateReservationRequest", 
    "ReservationFilterRequest",
    "OrderNumberRequest",
    "CustomerDataRequest",
    "BranchDataRequest",
    "SectorDataRequest",
    "CreateBranchScheduleRequest",
    "UpdateBranchScheduleRequest",
    "GetAvailableSlotsRequest",
    "GetBranchSchedulesRequest"
]
