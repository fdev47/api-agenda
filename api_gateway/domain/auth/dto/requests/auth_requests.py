"""
DTOs de requests para autenticación en el API Gateway
"""
from pydantic import BaseModel, Field, EmailStr


class ChangePasswordRequest(BaseModel):
    """DTO para cambiar contraseña de usuario"""
    email: EmailStr = Field(..., description="Email del usuario")
    new_password: str = Field(..., min_length=6, description="Nueva contraseña del usuario")

