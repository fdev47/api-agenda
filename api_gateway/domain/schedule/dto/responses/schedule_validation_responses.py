"""
DTOs de respuestas de validación para schedule en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class ImpactAnalysisResponse(BaseModel):
    """DTO para análisis de impacto"""
    affected_reservations: int = Field(..., description="Número de reservas afectadas")
    affected_customers: int = Field(..., description="Número de clientes afectados")
    total_impact: str = Field(..., description="Impacto total de la operación")


class ValidateScheduleDeletionResponse(BaseModel):
    """DTO para respuesta de validación de eliminación"""
    can_delete: bool = Field(..., description="Indica si se puede eliminar")
    requires_rescheduling: bool = Field(..., description="Requiere reagendar reservas")
    message: str = Field(..., description="Mensaje de validación")
    impact_analysis: Optional[ImpactAnalysisResponse] = Field(None, description="Análisis de impacto") 