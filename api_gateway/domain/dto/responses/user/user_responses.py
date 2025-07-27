"""
DTOs de respuesta para el API Gateway
"""
from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from uuid import UUID
from datetime import datetime


class RoleResponse(BaseModel):
    """Respuesta de rol"""
    id: UUID
    name: str
    description: Optional[str] = None


class ProfileResponse(BaseModel):
    """Respuesta de perfil"""
    id: UUID
    name: str
    description: Optional[str] = None
    roles: List[RoleResponse] = []


class AddressResponse(BaseModel):
    """Respuesta de dirección"""
    id: UUID
    street: str
    city_id: UUID
    state_id: UUID
    country_id: UUID
    postal_code: Optional[str] = None
    additional_info: Optional[str] = None


class CustomerResponse(BaseModel):
    """Respuesta de cliente"""
    id: UUID
    auth_uid: str
    ruc: str
    company_name: str
    email: str
    phone: Optional[str] = None
    cellphone_number: Optional[str] = None
    cellphone_country_code: Optional[str] = None
    is_active: bool
    profiles: List[ProfileResponse] = []
    address: Optional[AddressResponse] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserResponse(BaseModel):
    """Respuesta de usuario desde API Gateway"""
    id: UUID
    auth_uid: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    cellphone_number: Optional[str] = None
    cellphone_country_code: Optional[str] = None
    is_active: bool
    user_type: str  # 'admin' | 'user'
    profiles: List[ProfileResponse] = []
    customer: Optional[CustomerResponse] = None


class UserListResponse(BaseModel):
    """Respuesta de lista de usuarios desde API Gateway"""
    users: List[UserResponse]
    total: int
    page: int
    size: int


class SuccessResponse(BaseModel):
    """Respuesta de éxito genérica"""
    message: str
    timestamp: str 