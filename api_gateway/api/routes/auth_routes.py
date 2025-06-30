"""
Rutas de autenticación del API Gateway
"""
from fastapi import APIRouter, Depends, Header
from typing import Optional

router = APIRouter()


@router.get("/validate-token")
async def validate_token(authorization: Optional[str] = Header(None)):
    """
    Validar token de Firebase
    Redirige la validación al Auth Service
    """
    # Esta ruta redirige al Auth Service
    # La implementación real se hace en el middleware
    return {"message": "Use Auth Service directly for token validation"}


@router.get("/user-info")
async def get_user_info(authorization: Optional[str] = Header(None)):
    """
    Obtener información del usuario autenticado
    Redirige al Auth Service
    """
    # Esta ruta redirige al Auth Service
    return {"message": "Use Auth Service directly for user info"} 