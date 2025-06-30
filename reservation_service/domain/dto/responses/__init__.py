# Reservation Service response DTOs

from .reservation_responses import (
    ReservationResponse,
    ReservationListResponse,
    ReservationSummaryResponse,
    ReservationSummaryListResponse,
    OrderNumberResponse,
    CustomerDataResponse,
    BranchDataResponse,
    SectorDataResponse
)
from .schedule_responses import (
    TimeSlotResponse,
    BranchScheduleResponse,
    AvailableSlotsResponse,
    BranchScheduleListResponse,
    CreateBranchScheduleResponse,
    UpdateBranchScheduleResponse,
    DeleteBranchScheduleResponse
)

__all__ = [
    "ReservationResponse",
    "ReservationListResponse",
    "ReservationSummaryResponse",
    "ReservationSummaryListResponse",
    "OrderNumberResponse",
    "CustomerDataResponse",
    "BranchDataResponse",
    "SectorDataResponse",
    "TimeSlotResponse",
    "BranchScheduleResponse",
    "AvailableSlotsResponse",
    "BranchScheduleListResponse",
    "CreateBranchScheduleResponse",
    "UpdateBranchScheduleResponse",
    "DeleteBranchScheduleResponse"
]
