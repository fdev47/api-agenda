"""
DTOs de requests para customers en el API Gateway
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class AddressData(BaseModel):
    """Datos de dirección para customer"""
    street: str = Field(..., description="Calle y número")
    city_id: int = Field(..., description="ID de la ciudad")
    state_id: int = Field(..., description="ID del estado")
    country_id: int = Field(..., description="ID del país")
    postal_code: Optional[str] = Field(None, description="Código postal")
    additional_info: Optional[str] = Field(None, description="Información adicional")


class CreateCustomerRequest(BaseModel):
    """DTO para crear un customer desde el API Gateway"""
    email: EmailStr = Field(..., description="Email del customer")
    password: str = Field(..., min_length=6, description="Contraseña del customer")
    ruc: str = Field(..., min_length=5, max_length=11, description="RUC de la empresa")
    company_name: str = Field(..., min_length=3, description="Nombre de la empresa")
    username: Optional[str] = Field(None, description="Nombre de usuario del customer")
    phone: Optional[str] = Field(None, description="Teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    address: AddressData = Field(..., description="Datos de la dirección")
    is_active: bool = Field(default=True, description="Estado activo del customer")
    two_factor_enabled: bool = Field(default=False, description="Habilitar autenticación de dos factores")
    send_email_verification: bool = Field(default=True, description="Enviar email de verificación")


class UpdateCustomerRequest(BaseModel):
    """DTO para actualizar un customer desde el API Gateway"""
    email: Optional[EmailStr] = Field(None, description="Email del customer")
    ruc: Optional[str] = Field(None, min_length=5, max_length=11, description="RUC de la empresa")
    company_name: Optional[str] = Field(None, min_length=3, description="Nombre de la empresa")
    phone: Optional[str] = Field(None, description="Teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    address: Optional[AddressData] = Field(None, description="Datos de la dirección")
    is_active: Optional[bool] = Field(None, description="Estado activo del customer") 