"""
DTOs de responses para customers en el API Gateway
"""
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List


class CustomerResponse(BaseModel):
    """Response para un customer"""
    id: UUID = Field(..., description="Identificador único del customer")
    auth_uid: str = Field(..., description="UID de Firebase")
    ruc: str = Field(..., description="RUC de la empresa")
    company_name: str = Field(..., description="Nombre de la empresa")
    email: str = Field(..., description="Email del customer")
    username: Optional[str] = Field(None, description="Username del customer")
    phone: Optional[str] = Field(None, description="Teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    address_id: Optional[UUID] = Field(None, description="ID de la dirección")
    is_active: bool = Field(..., description="Estado activo del customer")


class CustomerListResponse(BaseModel):
    """Response para lista de customers"""
    customers: List[CustomerResponse] = Field(..., description="Lista de customers")
    total: int = Field(..., description="Total de customers")
    skip: int = Field(..., description="Número de elementos omitidos")
    limit: int = Field(..., description="Límite de elementos por página")


class CustomerUpdatedResponse(BaseModel):
    """Response para customer actualizado"""
    id: UUID = Field(..., description="Identificador único del customer")
    auth_uid: str = Field(..., description="UID de Firebase")
    ruc: str = Field(..., description="RUC de la empresa")
    company_name: str = Field(..., description="Nombre de la empresa")
    email: str = Field(..., description="Email del customer")
    username: Optional[str] = Field(None, description="Username del customer")
    phone: Optional[str] = Field(None, description="Teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    address_id: Optional[UUID] = Field(None, description="ID de la dirección")
    is_active: bool = Field(..., description="Estado activo del customer")
    message: str = Field(..., description="Mensaje de confirmación")


class CustomerDeletedResponse(BaseModel):
    """Response para customer eliminado"""
    message: str = Field(..., description="Mensaje de confirmación")
    customer_id: UUID = Field(..., description="ID del customer eliminado") 