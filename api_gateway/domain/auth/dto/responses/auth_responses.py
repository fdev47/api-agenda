"""
DTOs de responses para autenticación en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional


class ChangePasswordResponse(BaseModel):
    """DTO para respuesta de cambio de contraseña por email"""
    success: bool = Field(..., description="Indica si el cambio fue exitoso")
    message: str = Field(..., description="Mensaje de respuesta")
    email: str = Field(..., description="Email del usuario")


class ChangePasswordByUsernameResponse(BaseModel):
    """DTO para respuesta de cambio de contraseña por username"""
    success: bool = Field(..., description="Indica si el cambio fue exitoso")
    message: str = Field(..., description="Mensaje de respuesta")
    username: str = Field(..., description="Username del usuario o customer")
    user_type: str = Field(..., description="Tipo de usuario (user o customer)")

