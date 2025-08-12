"""
DTO de response para datos de cliente en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional


class CustomerDataResponse(BaseModel):
    """DTO para datos de cliente"""
    customer_id: Optional[int] = Field(None, description="ID del cliente en el sistema")
    id: Optional[str] = Field(None, description="UUID del cliente")
    auth_uid: Optional[str] = Field(None, description="UID de Firebase")
    ruc: Optional[str] = Field(None, description="RUC de la empresa")
    company_name: Optional[str] = Field(None, description="Nombre de la empresa")
    email: Optional[str] = Field(None, description="Email del cliente")
    username: Optional[str] = Field(None, description="Username del cliente")
    phone: Optional[str] = Field(None, description="Teléfono del cliente")
    cellphone_number: Optional[str] = Field(None, description="Celular del cliente")
    cellphone_country_code: Optional[str] = Field(None, description="Código de país del celular")
    address_id: Optional[str] = Field(None, description="ID de la dirección")
    is_active: Optional[bool] = Field(None, description="Estado activo del cliente") 