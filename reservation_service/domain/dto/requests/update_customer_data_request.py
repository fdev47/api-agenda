"""
Request DTO para actualización parcial de datos de cliente
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID


class UpdateCustomerDataRequest(BaseModel):
    """Request para actualización parcial de datos del cliente"""
    model_config = ConfigDict(from_attributes=True)
    
    # Todos los campos son opcionales para permitir actualización granular
    customer_id: Optional[int] = Field(None, gt=0, description="ID del cliente")
    id: Optional[UUID] = Field(None, description="UUID del cliente")
    auth_uid: Optional[str] = Field(None, description="UID de autenticación")
    ruc: Optional[str] = Field(None, min_length=10, max_length=15, description="RUC del cliente")
    company_name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nombre de la empresa")
    email: Optional[str] = Field(None, description="Email del cliente")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Nombre de usuario")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono del cliente")
    cellphone_number: Optional[str] = Field(None, max_length=20, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, max_length=5, description="Código de país del celular")
    address_id: Optional[UUID] = Field(None, description="UUID de la dirección")
    is_active: Optional[bool] = Field(None, description="Estado activo del cliente") 