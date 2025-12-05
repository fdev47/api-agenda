"""
DTOs de requests para autenticación en el API Gateway
"""
from pydantic import BaseModel, Field, EmailStr


class ChangePasswordRequest(BaseModel):
    """DTO para cambiar contraseña de usuario por email"""
    email: EmailStr = Field(..., description="Email del usuario")
    new_password: str = Field(..., min_length=6, description="Nueva contraseña del usuario")


class ChangePasswordByUsernameUserRequest(BaseModel):
    """DTO para cambiar contraseña de usuario por username"""
    username: str = Field(..., description="Username del usuario")
    new_password: str = Field(..., min_length=6, description="Nueva contraseña del usuario")


class ChangePasswordByUsernameCustomerRequest(BaseModel):
    """DTO para cambiar contraseña de cliente por username"""
    username: str = Field(..., description="Username del cliente")
    new_password: str = Field(..., min_length=6, description="Nueva contraseña del cliente")

