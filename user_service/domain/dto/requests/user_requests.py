"""
DTOs de requests para usuarios
"""
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from uuid import UUID
from enum import Enum

class UserType(str, Enum):
    """Tipos de usuario interno disponibles"""
    ADMIN = "admin"
    USER = "user"

class CreateUserRequest(BaseModel):
    """DTO para crear un usuario interno"""
    auth_uid: str = Field(..., description="UID del proveedor de autenticación")
    email: EmailStr = Field(..., description="Email del usuario")
    first_name: Optional[str] = Field(None, description="Nombre del usuario")
    last_name: Optional[str] = Field(None, description="Apellido del usuario")
    phone: Optional[str] = Field(None, description="Número de teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular (+52, +1, etc.)")
    user_type: UserType = Field(..., description="Tipo de usuario interno")
    is_active: bool = Field(True, description="Estado activo del usuario")

class UpdateUserRequest(BaseModel):
    """DTO para actualizar un usuario interno"""
    first_name: Optional[str] = Field(None, description="Nombre del usuario")
    last_name: Optional[str] = Field(None, description="Apellido del usuario")
    phone: Optional[str] = Field(None, description="Número de teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular (+52, +1, etc.)")
    is_active: Optional[bool] = Field(None, description="Estado activo del usuario")
    user_type: Optional[UserType] = Field(None, description="Tipo de usuario interno") 