"""
DTOs de responses de error para el dominio de usuarios
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ErrorResponse(BaseModel):
    """DTO para respuestas de error"""
    error: str = Field(..., description="Tipo de error")
    message: str = Field(..., description="Mensaje de error")
    error_code: Optional[str] = Field(None, description="Código de error específico")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp del error")
    details: Optional[dict] = Field(None, description="Detalles adicionales del error")
    request_id: Optional[str] = Field(None, description="ID de la request para tracking")

class ValidationErrorResponse(BaseModel):
    """DTO para errores de validación"""
    error: str = Field(default="validation_error", description="Tipo de error")
    message: str = Field(..., description="Mensaje de error")
    field_errors: list = Field(..., description="Lista de errores por campo")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp del error")
    request_id: Optional[str] = Field(None, description="ID de la request para tracking") 