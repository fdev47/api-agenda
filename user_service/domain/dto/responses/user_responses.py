"""
DTOs de responses para usuarios
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from uuid import UUID
from enum import Enum

class UserType(str, Enum):
    """Tipos de usuario interno disponibles"""
    ADMIN = "admin"
    USER = "user"

class UserResponse(BaseModel):
    """DTO para respuesta de usuario interno"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    auth_uid: str
    email: str
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    cellphone_number: Optional[str]
    cellphone_country_code: Optional[str]
    is_active: bool
    user_type: UserType
    # Removemos la referencia circular por ahora
    # profiles: List["ProfileResponse"] = []

class UserListResponse(BaseModel):
    """DTO para lista de usuarios internos"""
    users: List[UserResponse]
    total: int
    page: int
    size: int

# Actualizar referencias circulares
UserResponse.model_rebuild() 