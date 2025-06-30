"""
DTOs de responses para roles
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID

class RoleResponse(BaseModel):
    """DTO para respuesta de rol"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str] 