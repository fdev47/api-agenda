"""
DTOs de error responses para el dominio de ubicaciones
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ErrorResponse(BaseModel):
    """Response estándar para errores"""
    error: str = Field(..., description="Tipo de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    error_code: Optional[str] = Field(None, description="Código de error específico")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalles adicionales del error")
    timestamp: Optional[str] = Field(None, description="Timestamp del error")


class ValidationErrorResponse(BaseModel):
    """Response para errores de validación"""
    error: str = Field(default="validation_error", description="Tipo de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    field_errors: Dict[str, str] = Field(..., description="Errores por campo")
    timestamp: Optional[str] = Field(None, description="Timestamp del error")


class LocationErrorResponse(BaseModel):
    """Response específico para errores de ubicaciones"""
    error: str = Field(default="location_error", description="Tipo de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    error_code: Optional[str] = Field(None, description="Código de error específico")
    entity_type: Optional[str] = Field(None, description="Tipo de entidad (country, state, city, local, branch)")
    entity_id: Optional[int] = Field(None, description="ID de la entidad relacionada")
    timestamp: Optional[str] = Field(None, description="Timestamp del error")


class NotFoundErrorResponse(BaseModel):
    """Response específico para errores de entidad no encontrada"""
    error: str = Field(default="not_found", description="Tipo de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    entity_type: str = Field(..., description="Tipo de entidad no encontrada")
    entity_id: Optional[int] = Field(None, description="ID de la entidad no encontrada")
    timestamp: Optional[str] = Field(None, description="Timestamp del error")


class ConflictErrorResponse(BaseModel):
    """Response específico para errores de conflicto (duplicados)"""
    error: str = Field(default="conflict", description="Tipo de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    entity_type: str = Field(..., description="Tipo de entidad en conflicto")
    field_name: Optional[str] = Field(None, description="Campo que causa el conflicto")
    field_value: Optional[str] = Field(None, description="Valor que causa el conflicto")
    timestamp: Optional[str] = Field(None, description="Timestamp del error") 