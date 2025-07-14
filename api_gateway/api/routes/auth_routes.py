"""
Rutas de autenticación del API Gateway
"""
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from typing import Optional
from datetime import datetime
import logging

from api_gateway.config import GatewayConfig
from api_gateway.middleware import auth_middleware

router = APIRouter()


@router.get("/validate-token")
async def validate_token(request: Request, authorization: Optional[str] = Header(None)):
    """
    Validar token de Firebase
    
    Esta ruta valida el token usando el Auth Service.
    
    Args:
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información del usuario si el token es válido
    """
    # Usar el middleware para validar el token
    try:
        user = await auth_middleware.validate_auth(request, authorization)
        return {
            "valid": True,
            "message": "Token válido",
            "user": user,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException as e:
        # Re-lanzar la excepción con el formato correcto
        raise e


@router.get("/user-info")
async def get_user_info(request: Request, authorization: Optional[str] = Header(None)):
    """
    Obtener información del usuario autenticado
    
    Esta ruta valida el token y retorna la información del usuario.
    
    Args:
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información del usuario autenticado
    """
    # Usar el middleware para validar el token
    try:
        user = await auth_middleware.validate_auth(request, authorization)
        return {
            "valid": True,
            "message": "Usuario autenticado",
            "user": user,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException as e:
        # Re-lanzar la excepción con el formato correcto
        raise e


@router.get("/login")
async def login_redirect():
    """
    Redirigir al endpoint de login del Auth Service
    
    Returns:
        dict: Información sobre el endpoint de login
    """
    auth_service_url = GatewayConfig.AUTH_SERVICE_URL
    
    return {
        "message": "Use Auth Service directly for login",
        "auth_service_url": f"{auth_service_url}/login",
        "documentation": f"{auth_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": "/login"
    }


@router.get("/refresh-token")
async def refresh_token_redirect():
    """
    Redirigir al endpoint de refresh token del Auth Service
    
    Returns:
        dict: Información sobre el endpoint de refresh token
    """
    auth_service_url = GatewayConfig.AUTH_SERVICE_URL
    
    return {
        "message": "Use Auth Service directly for refresh token",
        "auth_service_url": f"{auth_service_url}/refresh-token",
        "documentation": f"{auth_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": "/refresh-token"
    } 