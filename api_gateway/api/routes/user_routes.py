"""
Rutas de usuarios del API Gateway
"""
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from typing import Optional
from datetime import datetime
import logging

from api_gateway.config import GatewayConfig
from api_gateway.middleware import auth_middleware

router = APIRouter()


@router.get("/")
async def list_users(request: Request, authorization: Optional[str] = Header(None)):
    """
    Listar usuarios
    
    Esta ruta requiere autenticación y valida el token.
    
    Args:
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación
    await auth_middleware.validate_auth(request, authorization)
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for user operations",
        "user_service_url": f"{user_service_url}/users",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": "/users"
    }


@router.post("/")
async def create_user(request: Request, authorization: Optional[str] = Header(None)):
    """
    Crear usuario
    
    Esta ruta requiere autenticación y valida el token.
    
    Args:
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación
    await auth_middleware.validate_auth(request, authorization)
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for user operations",
        "user_service_url": f"{user_service_url}/users",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": "/users"
    }


@router.get("/{user_id}")
async def get_user(user_id: str, request: Request, authorization: Optional[str] = Header(None)):
    """
    Obtener usuario por ID
    
    Esta ruta requiere autenticación y valida el token.
    
    Args:
        user_id: ID del usuario a obtener
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación
    await auth_middleware.validate_auth(request, authorization)
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for user operations",
        "user_service_url": f"{user_service_url}/users/{user_id}",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": f"/users/{user_id}",
        "user_id": user_id
    }


@router.put("/{user_id}")
async def update_user(user_id: str, request: Request, authorization: Optional[str] = Header(None)):
    """
    Actualizar usuario
    
    Esta ruta requiere autenticación y valida el token.
    
    Args:
        user_id: ID del usuario a actualizar
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación
    await auth_middleware.validate_auth(request, authorization)
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for user operations",
        "user_service_url": f"{user_service_url}/users/{user_id}",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": f"/users/{user_id}",
        "user_id": user_id
    }


@router.delete("/{user_id}")
async def delete_user(user_id: str, request: Request, authorization: Optional[str] = Header(None)):
    """
    Eliminar usuario
    
    Esta ruta requiere autenticación y valida el token.
    
    Args:
        user_id: ID del usuario a eliminar
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación
    await auth_middleware.validate_auth(request, authorization)
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for user operations",
        "user_service_url": f"{user_service_url}/users/{user_id}",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": f"/users/{user_id}",
        "user_id": user_id
    }


@router.get("/profile/{user_id}")
async def get_user_profile(user_id: str, request: Request, authorization: Optional[str] = Header(None)):
    """
    Obtener perfil de usuario
    
    Esta ruta requiere autenticación y valida el token.
    
    Args:
        user_id: ID del usuario
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación
    await auth_middleware.validate_auth(request, authorization)
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for user profile operations",
        "user_service_url": f"{user_service_url}/users/{user_id}/profile",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": f"/users/{user_id}/profile",
        "user_id": user_id
    }


@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str, request: Request, authorization: Optional[str] = Header(None)):
    """
    Obtener cliente por ID
    
    Esta ruta requiere autenticación y valida el token.
    
    Args:
        customer_id: ID del cliente a obtener
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación
    await auth_middleware.validate_auth(request, authorization)
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for customer operations",
        "user_service_url": f"{user_service_url}/customers/{customer_id}",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": f"/customers/{customer_id}",
        "customer_id": customer_id
    } 