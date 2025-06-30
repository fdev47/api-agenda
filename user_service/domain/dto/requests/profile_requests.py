"""
DTOs de requests para perfiles
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class CreateProfileRequest(BaseModel):
    """DTO para crear un perfil"""
    name: str = Field(..., description="Nombre del perfil")
    description: Optional[str] = Field(None, description="Descripción del perfil")
    role_ids: List[UUID] = Field(default=[], description="IDs de roles a asignar")

class UpdateProfileRequest(BaseModel):
    """DTO para actualizar un perfil"""
    name: Optional[str] = Field(None, description="Nombre del perfil")
    description: Optional[str] = Field(None, description="Descripción del perfil")
    role_ids: Optional[List[UUID]] = Field(None, description="IDs de roles a asignar") 