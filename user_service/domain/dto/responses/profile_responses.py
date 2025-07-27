"""
DTOs de responses para perfiles
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from uuid import UUID

class ProfileResponse(BaseModel):
    """DTO para respuesta de perfil"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str]
    # Removemos la referencia circular por ahora
    # roles: List["RoleResponse"] = []


class ProfileListResponse(BaseModel):
    """DTO para lista de perfiles"""
    profiles: List[ProfileResponse]
    total: int
    skip: int
    limit: int 