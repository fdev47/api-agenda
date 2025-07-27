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
    """DTO para crear usuario"""
    auth_uid: str = Field(..., description="UID del proveedor de autenticación")
    email: EmailStr = Field(..., description="Email del usuario")
    username: Optional[str] = Field(None, description="Nombre de usuario")  # Nuevo campo
    first_name: Optional[str] = Field(None, description="Nombre del usuario")
    last_name: Optional[str] = Field(None, description="Apellido del usuario")
    phone: Optional[str] = Field(None, description="Número de teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    is_active: bool = Field(True, description="Estado activo del usuario")
    user_type: UserType = Field(..., description="Tipo de usuario")
    profile_ids: List[UUID] = Field(default=[], description="IDs de perfiles a asignar")

class UpdateUserRequest(BaseModel):
    """DTO para actualizar un usuario interno"""
    first_name: Optional[str] = Field(None, description="Nombre del usuario")
    last_name: Optional[str] = Field(None, description="Apellido del usuario")
    phone: Optional[str] = Field(None, description="Número de teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular (+52, +1, etc.)")
    is_active: Optional[bool] = Field(None, description="Estado activo del usuario")
    user_type: Optional[UserType] = Field(None, description="Tipo de usuario interno") 