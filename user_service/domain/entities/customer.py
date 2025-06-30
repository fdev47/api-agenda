"""
Entidad Customer del dominio - Clientes que reservan en el sistema
"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
from typing import List, Optional
from datetime import datetime
from .profile import Profile
from .address import Address

class Customer(BaseModel):
    """Entidad Customer del dominio - Clientes que reservan en el sistema"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(default_factory=uuid4, description="Identificador único del cliente")
    auth_uid: str = Field(..., description="UID del proveedor de autenticación")
    ruc: str = Field(..., description="RUC del cliente")
    company_name: str = Field(..., description="Razón Social")
    email: str = Field(..., description="Email del cliente")
    phone: str | None = Field(None, description="Número de teléfono fijo")
    cellphone_number: str | None = Field(None, description="Número de celular")
    cellphone_country_code: str | None = Field(None, description="Código de país del celular (+52, +1, etc.)")
    is_active: bool = Field(True, description="Estado activo del cliente")
    profiles: List[Profile] = Field(default=[], description="Perfiles del cliente")
    address: Optional[Address] = Field(None, description="Dirección del cliente")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización") 