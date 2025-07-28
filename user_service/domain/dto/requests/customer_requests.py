"""
DTOs de requests para Customer
"""
from pydantic import BaseModel, Field
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
    """Request para crear un customer"""
    auth_uid: str = Field(..., description="UID de Firebase")
    ruc: str = Field(..., description="RUC de la empresa")
    company_name: str = Field(..., description="Nombre de la empresa")
    email: str = Field(..., description="Email del customer")
    username: Optional[str] = Field(None, description="Username del customer")
    phone: Optional[str] = Field(None, description="Teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    address: AddressData = Field(..., description="Datos de la dirección")
    is_active: bool = Field(True, description="Estado activo del customer")

class UpdateCustomerRequest(BaseModel):
    """Request para actualizar un customer"""
    ruc: Optional[str] = Field(None, description="RUC de la empresa")
    company_name: Optional[str] = Field(None, description="Nombre de la empresa")
    email: Optional[str] = Field(None, description="Email del customer")
    username: Optional[str] = Field(None, description="Username del customer")
    phone: Optional[str] = Field(None, description="Teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    address: Optional[AddressData] = Field(None, description="Datos de la dirección")
    is_active: Optional[bool] = Field(None, description="Estado activo del customer") 