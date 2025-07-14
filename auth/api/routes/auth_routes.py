"""
Rutas de autenticación para Firebase Auth
"""
from fastapi import APIRouter, Depends, Header
from typing import Optional
from ...domain.dto.requests import CreateUserRequest
from ...domain.dto.responses import UserInfoResponse
from ...infrastructure.container import container

router = APIRouter()


@router.get("/validate-token")
async def validate_token_header(authorization: Optional[str] = Header(None)):
    """
    Validar token de Firebase desde header Authorization
    Endpoint para uso de otros servicios
    """
    if not authorization or not authorization.startswith("Bearer "):
        return {
            "valid": False,
            "message": "Token no proporcionado o formato incorrecto",
            "user": None
        }
    
    token = authorization.replace("Bearer ", "")
    
    try:
        validate_use_case = container.validate_token_use_case()
        user = validate_use_case.execute(token)
        return {
            "valid": True,
            "message": "Token válido",
            "user": {
                "user_id": user.user_id,
                "email": user.email,
                "display_name": user.display_name,
                "email_verified": user.email_verified,
                "custom_claims": user.custom_claims,
                "created_at": user.created_at.isoformat(),
                "last_sign_in": user.last_sign_in.isoformat() if user.last_sign_in else None
            }
        }
    except Exception as e:
        return {
            "valid": False,
            "message": str(e),
            "user": None
        }


@router.get("/user-info")
async def get_user_info(authorization: Optional[str] = Header(None)):
    """
    Obtener información del usuario autenticado
    """
    if not authorization or not authorization.startswith("Bearer "):
        return {
            "valid": False,
            "message": "Token no proporcionado o formato incorrecto",
            "user": None
        }
    
    token = authorization.replace("Bearer ", "")
    
    try:
        validate_use_case = container.validate_token_use_case()
        user = validate_use_case.execute(token)
        return UserInfoResponse.model_validate(user)
    except Exception as e:
        return {
            "valid": False,
            "message": str(e),
            "user": None
        }


@router.post("/create-user", response_model=UserInfoResponse)
async def create_user_in_firebase(request: CreateUserRequest):
    """
    Crear usuario en Firebase
    Endpoint para uso interno de user_service
    """
    try:
        # Crear usuario en Firebase
        user = container.auth_provider.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name
        )
        
        return UserInfoResponse.model_validate(user)
    except Exception as e:
        # Re-lanzar la excepción para que user_service la maneje
        raise e 