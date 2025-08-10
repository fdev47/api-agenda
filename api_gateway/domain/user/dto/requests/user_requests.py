"""
DTOs de requests para usuarios en el API Gateway
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from uuid import UUID


class CreateUserRequest(BaseModel):
    """DTO para crear un usuario desde el API Gateway"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")
    username: Optional[str] = Field(None, description="Nombre de usuario")
    first_name: Optional[str] = Field(None, description="Nombre del usuario")
    last_name: Optional[str] = Field(None, description="Apellido del usuario")
    phone: Optional[str] = Field(None, description="Teléfono del usuario")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    is_active: bool = Field(default=True, description="Estado activo del usuario")
    user_type: str = Field(default="customer", description="Tipo de usuario")
    profile_ids: Optional[List[UUID]] = Field(default=[], description="IDs de perfiles a asignar")
    two_factor_enabled: bool = Field(default=False, description="Habilitar autenticación de dos factores")
    send_email_verification: bool = Field(default=True, description="Enviar email de verificación")


class UpdateUserRequest(BaseModel):
    """DTO para actualizar un usuario desde el API Gateway"""
    email: Optional[EmailStr] = Field(None, description="Email del usuario")
    first_name: Optional[str] = Field(None, description="Nombre del usuario")
    last_name: Optional[str] = Field(None, description="Apellido del usuario")
    phone: Optional[str] = Field(None, description="Teléfono del usuario")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    is_active: Optional[bool] = Field(None, description="Estado activo del usuario")
    user_type: Optional[str] = Field(None, description="Tipo de usuario")
    profile_ids: Optional[List[UUID]] = Field(None, description="IDs de perfiles a asignar") 