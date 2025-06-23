"""API schemas using Pydantic"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Dict, Any, List


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: Optional[str] = None
    phone_number: Optional[str] = None
    initial_role: str = "user"
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v


class ValidateTokenRequest(BaseModel):
    token: str


class AssignRoleRequest(BaseModel):
    user_id: str
    role: str


class AssignPermissionRequest(BaseModel):
    user_id: str
    permission: str


class UserResponse(BaseModel):
    user_id: str
    email: str
    display_name: Optional[str]
    phone_number: Optional[str]
    email_verified: bool
    roles: List[str]
    permissions: List[str]
    organization_id: Optional[str]
    created_at: str
    last_sign_in: Optional[str]


class ErrorResponse(BaseModel):
    error: str
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None 