"""
Response DTO para datos del cliente
"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional


class CustomerDataResponse(BaseModel):
    """Response para datos del cliente"""
    model_config = ConfigDict(from_attributes=True)
    
    # ID de referencia (opcional, puede no existir en el sistema)
    customer_id: Optional[int] = Field(None, description="ID del cliente en el sistema")
    
    # Datos completos al momento de la reserva (mismos campos que Customer)
    id: Optional[UUID] = Field(None, description="Identificador único del customer")
    auth_uid: Optional[str] = Field(None, description="UID de Firebase")
    ruc: str = Field(..., description="RUC de la empresa")
    company_name: str = Field(..., description="Nombre de la empresa")
    email: str = Field(..., description="Email del customer")
    username: Optional[str] = Field(None, description="Username del customer")
    phone: Optional[str] = Field(None, description="Teléfono fijo")
    cellphone_number: Optional[str] = Field(None, description="Número de celular")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    address_id: Optional[UUID] = Field(None, description="ID de la dirección")
    is_active: bool = Field(True, description="Estado activo del customer") 