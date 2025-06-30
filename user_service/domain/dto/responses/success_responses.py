"""
DTOs de responses de éxito para el dominio de usuarios
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SuccessResponse(BaseModel):
    """DTO para respuestas de éxito genéricas"""
    success: bool = Field(default=True, description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de confirmación")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp de la respuesta")

class MessageResponse(BaseModel):
    """DTO para respuestas con mensaje simple"""
    message: str = Field(..., description="Mensaje de la respuesta")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp de la respuesta")

class RoleAssignmentResponse(BaseModel):
    """DTO para respuesta de asignación de rol"""
    success: bool = Field(default=True, description="Indica si la asignación fue exitosa")
    message: str = Field(..., description="Mensaje de confirmación")
    user_id: str = Field(..., description="ID del usuario")
    role: str = Field(..., description="Rol asignado")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp de la respuesta")

class PermissionAssignmentResponse(BaseModel):
    """DTO para respuesta de asignación de permiso"""
    success: bool = Field(default=True, description="Indica si la asignación fue exitosa")
    message: str = Field(..., description="Mensaje de confirmación")
    user_id: str = Field(..., description="ID del usuario")
    permission: str = Field(..., description="Permiso asignado")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp de la respuesta")

class UserRolesResponse(BaseModel):
    """DTO para respuesta de roles de usuario"""
    user_id: str = Field(..., description="ID del usuario")
    roles: List[str] = Field(..., description="Lista de roles del usuario")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp de la respuesta") 