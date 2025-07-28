"""
Entidad Customer del dominio
"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
from typing import Optional

class Customer(BaseModel):
    """Entidad Customer del dominio"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(default_factory=uuid4, description="Identificador único del customer")
    auth_uid: str = Field(..., description="UID de Firebase")
    ruc: str = Field(..., description="RUC de la empresa")
    company_name: str = Field(..., description="Nombre de la empresa")
    email: str = Field(..., description="Email del customer")
    username: Optional[str] = Field(None, description="Username del customer")
    phone: Optional[str] = Field(None, description="Teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    address_id: Optional[UUID] = Field(None, description="ID de la dirección")
    is_active: bool = Field(True, description="Estado activo del customer") 