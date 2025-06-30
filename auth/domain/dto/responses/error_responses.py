"""
DTOs de error responses para el dominio de autenticación
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


class AuthErrorResponse(BaseModel):
    """Response específico para errores de autenticación"""
    error: str = Field(default="auth_error", description="Tipo de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    error_code: Optional[str] = Field(None, description="Código de error específico")
    token_expired: Optional[bool] = Field(None, description="Indica si el token expiró")
    timestamp: Optional[str] = Field(None, description="Timestamp del error") 