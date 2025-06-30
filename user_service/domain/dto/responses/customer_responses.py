"""
DTOs de responses para clientes
"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from ...entities.address import Address
from ...entities.profile import Profile

class CustomerResponse(BaseModel):
    """Response para un cliente"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(..., description="Identificador único del cliente")
    ruc: str = Field(..., description="RUC del cliente")
    company_name: str = Field(..., description="Nombre de la empresa")
    email: str = Field(..., description="Email del cliente")
    phone: Optional[str] = Field(None, description="Número de teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    is_active: bool = Field(..., description="Estado activo del cliente")
    profiles: List[Profile] = Field(default=[], description="Perfiles del cliente")
    address: Optional[Address] = Field(None, description="Dirección del cliente")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

class CustomerListResponse(BaseModel):
    """Response para lista de clientes"""
    customers: List[CustomerResponse] = Field(..., description="Lista de clientes")
    total: int = Field(..., description="Total de clientes")
    skip: int = Field(..., description="Número de elementos omitidos")
    limit: int = Field(..., description="Límite de elementos por página") 