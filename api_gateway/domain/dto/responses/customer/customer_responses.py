"""
DTOs de responses para customers en el API Gateway
"""
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


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