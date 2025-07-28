"""
DTOs de responses para clientes
"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import List, Optional
from datetime import datetime

class CustomerResponse(BaseModel):
    """Response para un cliente"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(..., description="Identificador único del cliente")
    auth_uid: str = Field(..., description="UID de Firebase")
    ruc: str = Field(..., description="RUC del cliente")
    company_name: str = Field(..., description="Nombre de la empresa")
    email: str = Field(..., description="Email del cliente")
    username: Optional[str] = Field(None, description="Nombre de usuario del cliente")
    phone: Optional[str] = Field(None, description="Número de teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    address_id: Optional[UUID] = Field(None, description="ID de la dirección")
    is_active: bool = Field(..., description="Estado activo del cliente")

class CustomerListResponse(BaseModel):
    """Response para lista de clientes"""
    customers: List[CustomerResponse] = Field(..., description="Lista de clientes")
    total: int = Field(..., description="Total de clientes")
    skip: int = Field(..., description="Número de elementos omitidos")
    limit: int = Field(..., description="Límite de elementos por página") 

class CustomerUpdatedResponse(BaseModel):
    """Response para actualizar un cliente"""
    customer: CustomerResponse = Field(..., description="Cliente actualizado")
    message: str = Field(..., description="Mensaje de éxito")

class CustomerDeletedResponse(BaseModel):
    """Response para eliminar un cliente"""
    customer: CustomerResponse = Field(..., description="Cliente eliminado")
    message: str = Field(..., description="Mensaje de éxito")