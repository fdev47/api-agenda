"""
DTOs de responses para autenticación en el API Gateway
"""
from pydantic import BaseModel, Field


class ChangePasswordResponse(BaseModel):
    """DTO para respuesta de cambio de contraseña"""
    success: bool = Field(..., description="Indica si el cambio fue exitoso")
    message: str = Field(..., description="Mensaje de respuesta")
    email: str = Field(..., description="Email del usuario")

