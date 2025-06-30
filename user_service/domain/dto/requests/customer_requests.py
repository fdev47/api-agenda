"""
DTOs de requests para clientes
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from ...entities.address import Address

class CreateCustomerRequest(BaseModel):
    """Request para crear un cliente"""
    auth_uid: str = Field(..., description="UID del proveedor de autenticación")
    ruc: str = Field(..., description="RUC del cliente", min_length=11, max_length=11)
    company_name: str = Field(..., description="Nombre de la empresa", min_length=3)
    email: EmailStr = Field(..., description="Email del cliente")
    phone: Optional[str] = Field(None, description="Número de teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular (+52, +1, etc.)")
    address: Optional[Address] = Field(None, description="Dirección del cliente")

class UpdateCustomerRequest(BaseModel):
    """Request para actualizar un cliente"""
    ruc: Optional[str] = Field(None, description="RUC del cliente", min_length=11, max_length=11)
    company_name: Optional[str] = Field(None, description="Nombre de la empresa", min_length=3)
    email: Optional[EmailStr] = Field(None, description="Email del cliente")
    phone: Optional[str] = Field(None, description="Número de teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular (+52, +1, etc.)")
    address: Optional[Address] = Field(None, description="Dirección del cliente") 