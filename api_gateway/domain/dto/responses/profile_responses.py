"""
DTOs de respuestas para perfiles en el API Gateway
"""
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID

class ProfileResponse(BaseModel):
    """DTO para respuesta de perfil"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str] = None

class ProfileListResponse(BaseModel):
    """DTO para respuesta de lista de perfiles"""
    profiles: List[ProfileResponse]
    total: int
    skip: int
    limit: int 