"""
DTOs de requests para roles
"""
from pydantic import BaseModel, Field
from typing import Optional

class CreateRoleRequest(BaseModel):
    """DTO para crear un rol"""
    name: str = Field(..., description="Nombre del rol")
    description: Optional[str] = Field(None, description="Descripción del rol")

class UpdateRoleRequest(BaseModel):
    """DTO para actualizar un rol"""
    name: Optional[str] = Field(None, description="Nombre del rol")
    description: Optional[str] = Field(None, description="Descripción del rol") 