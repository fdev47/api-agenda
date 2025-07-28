"""
Response DTOs para validación de horarios
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from .schedule_responses import BranchScheduleResponse


class ScheduleInfoResponse(BaseModel):
    """Información del horario"""
    id: int
    branch_id: int
    day_of_week: int
    day_name: str
    current_schedule: Dict[str, Any]


class ImpactAnalysisResponse(BaseModel):
    """Análisis de impacto de cambios de horario"""
    total_reservations: int
    impacted_reservations: int
    safe_reservations: int
    impacted_reservation_ids: List[int]
    safe_reservation_ids: List[int]


class ValidateScheduleDeletionResponse(BaseModel):
    """Respuesta para validación de eliminación de horario"""
    message: str
    can_delete: bool
    requires_rescheduling: bool
    schedule_info: ScheduleInfoResponse
    impact_analysis: ImpactAnalysisResponse


class ValidateScheduleUpdateResponse(BaseModel):
    """Respuesta para validación de actualización de horario"""
    message: str
    schedule: Optional[Dict[str, Any]] = None
    impact_analysis: Optional[Dict[str, Any]] = None
    requires_confirmation: Optional[bool] = None


class ValidateScheduleChangesResult(BaseModel):
    """Resultado del use case ValidateScheduleChangesUseCase"""
    branch_id: int
    day_of_week: int
    day_name: str
    current_schedule: Dict[str, Any]
    proposed_changes: Dict[str, Any]
    impact_analysis: ImpactAnalysisResponse
    can_proceed: bool
    requires_rescheduling: bool


class DeleteScheduleWithValidationResult(BaseModel):
    """Resultado del use case DeleteBranchScheduleWithValidationUseCase.execute"""
    success: bool
    message: str
    schedule_id: Optional[int] = None
    impact_analysis: Optional[ValidateScheduleChangesResult] = None
    reservations_updated: Optional[int] = None
    requires_confirmation: Optional[bool] = None


class UpdateScheduleResult(BaseModel):
    """Resultado del use case UpdateBranchScheduleUseCase"""
    success: bool
    message: str
    schedule: Optional[BranchScheduleResponse] = None
    impact_analysis: Optional[ValidateScheduleChangesResult] = None
    reservations_updated: Optional[int] = None
    requires_confirmation: Optional[bool] = None 