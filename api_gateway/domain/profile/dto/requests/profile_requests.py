"""
DTOs de requests para perfiles en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class CreateProfileRequest(BaseModel):
    """DTO para crear un perfil desde el API Gateway"""
    name: str = Field(..., min_length=1, description="Nombre del perfil")
    description: Optional[str] = Field(None, description="Descripción del perfil")
    role_ids: Optional[List[UUID]] = Field(default=[], description="IDs de roles a asignar")


class UpdateProfileRequest(BaseModel):
    """DTO para actualizar un perfil desde el API Gateway"""
    name: Optional[str] = Field(None, min_length=1, description="Nombre del perfil")
    description: Optional[str] = Field(None, description="Descripción del perfil")
    role_ids: Optional[List[UUID]] = Field(None, description="IDs de roles a asignar") 