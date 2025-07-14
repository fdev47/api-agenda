"""
Rutas de administración del API Gateway
"""
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from typing import Optional
from datetime import datetime
import logging

from api_gateway.config import GatewayConfig
from api_gateway.middleware import auth_middleware

router = APIRouter()


@router.get("/users")
async def list_users_admin(request: Request, authorization: Optional[str] = Header(None)):
    """
    Listar usuarios (admin)
    
    Esta ruta requiere autenticación con rol admin.
    
    Args:
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación con rol admin
    user = await auth_middleware.validate_auth(request, authorization)
    
    # Verificar rol admin
    user_roles = user.get("custom_claims", {}).get("roles", [])
    if "admin" not in user_roles:
        request_id = getattr(request.state, 'request_id', None)
        
        from api_gateway.domain.dto.responses import ErrorResponse
        
        error_response = ErrorResponse(
            error="auth_error",
            message="Se requiere rol: admin",
            error_code="INSUFFICIENT_PERMISSIONS",
            timestamp=datetime.now().isoformat(),
            request_id=request_id
        )
        
        raise HTTPException(
            status_code=403,
            detail=error_response.model_dump()
        )
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for admin operations",
        "user_service_url": f"{user_service_url}/admin/users",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": "/admin/users"
    }


@router.post("/users/assign-role")
async def assign_role(request: Request, authorization: Optional[str] = Header(None)):
    """
    Asignar rol a usuario (admin)
    
    Esta ruta requiere autenticación con rol admin.
    
    Args:
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación con rol admin
    user = await auth_middleware.validate_auth(request, authorization)
    
    # Verificar rol admin
    user_roles = user.get("custom_claims", {}).get("roles", [])
    if "admin" not in user_roles:
        request_id = getattr(request.state, 'request_id', None)
        
        from api_gateway.domain.dto.responses import ErrorResponse
        
        error_response = ErrorResponse(
            error="auth_error",
            message="Se requiere rol: admin",
            error_code="INSUFFICIENT_PERMISSIONS",
            timestamp=datetime.now().isoformat(),
            request_id=request_id
        )
        
        raise HTTPException(
            status_code=403,
            detail=error_response.model_dump()
        )
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for admin operations",
        "user_service_url": f"{user_service_url}/admin/users/assign-role",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": "/admin/users/assign-role"
    }


@router.delete("/users/{user_id}")
async def delete_user_admin(user_id: str, request: Request, authorization: Optional[str] = Header(None)):
    """
    Eliminar usuario (admin)
    
    Esta ruta requiere autenticación con rol admin.
    
    Args:
        user_id: ID del usuario a eliminar
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación con rol admin
    user = await auth_middleware.validate_auth(request, authorization)
    
    # Verificar rol admin
    user_roles = user.get("custom_claims", {}).get("roles", [])
    if "admin" not in user_roles:
        request_id = getattr(request.state, 'request_id', None)
        
        from api_gateway.domain.dto.responses import ErrorResponse
        
        error_response = ErrorResponse(
            error="auth_error",
            message="Se requiere rol: admin",
            error_code="INSUFFICIENT_PERMISSIONS",
            timestamp=datetime.now().isoformat(),
            request_id=request_id
        )
        
        raise HTTPException(
            status_code=403,
            detail=error_response.model_dump()
        )
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for admin operations",
        "user_service_url": f"{user_service_url}/admin/users/{user_id}",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": f"/admin/users/{user_id}",
        "user_id": user_id
    }


@router.get("/roles")
async def list_roles_admin(request: Request, authorization: Optional[str] = Header(None)):
    """
    Listar roles (admin)
    
    Esta ruta requiere autenticación con rol admin.
    
    Args:
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación con rol admin
    user = await auth_middleware.validate_auth(request, authorization)
    
    # Verificar rol admin
    user_roles = user.get("custom_claims", {}).get("roles", [])
    if "admin" not in user_roles:
        request_id = getattr(request.state, 'request_id', None)
        
        from api_gateway.domain.dto.responses import ErrorResponse
        
        error_response = ErrorResponse(
            error="auth_error",
            message="Se requiere rol: admin",
            error_code="INSUFFICIENT_PERMISSIONS",
            timestamp=datetime.now().isoformat(),
            request_id=request_id
        )
        
        raise HTTPException(
            status_code=403,
            detail=error_response.model_dump()
        )
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for admin operations",
        "user_service_url": f"{user_service_url}/admin/roles",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": "/admin/roles"
    }


@router.post("/roles")
async def create_role_admin(request: Request, authorization: Optional[str] = Header(None)):
    """
    Crear rol (admin)
    
    Esta ruta requiere autenticación con rol admin.
    
    Args:
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de usuarios
    """
    # Validar autenticación con rol admin
    user = await auth_middleware.validate_auth(request, authorization)
    
    # Verificar rol admin
    user_roles = user.get("custom_claims", {}).get("roles", [])
    if "admin" not in user_roles:
        request_id = getattr(request.state, 'request_id', None)
        
        from api_gateway.domain.dto.responses import ErrorResponse
        
        error_response = ErrorResponse(
            error="auth_error",
            message="Se requiere rol: admin",
            error_code="INSUFFICIENT_PERMISSIONS",
            timestamp=datetime.now().isoformat(),
            request_id=request_id
        )
        
        raise HTTPException(
            status_code=403,
            detail=error_response.model_dump()
        )
    
    user_service_url = GatewayConfig.USER_SERVICE_URL
    
    return {
        "message": "Use User Service directly for admin operations",
        "user_service_url": f"{user_service_url}/admin/roles",
        "documentation": f"{user_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": "/admin/roles"
    }


@router.get("/auth/users")
async def list_auth_users_admin(request: Request, authorization: Optional[str] = Header(None)):
    """
    Listar usuarios de autenticación (admin)
    
    Esta ruta requiere autenticación con rol admin.
    
    Args:
        authorization: Header de autorización con el token Bearer
        
    Returns:
        dict: Información sobre el servicio de autenticación
    """
    # Validar autenticación con rol admin
    user = await auth_middleware.validate_auth(request, authorization)
    
    # Verificar rol admin
    user_roles = user.get("custom_claims", {}).get("roles", [])
    if "admin" not in user_roles:
        request_id = getattr(request.state, 'request_id', None)
        
        from api_gateway.domain.dto.responses import ErrorResponse
        
        error_response = ErrorResponse(
            error="auth_error",
            message="Se requiere rol: admin",
            error_code="INSUFFICIENT_PERMISSIONS",
            timestamp=datetime.now().isoformat(),
            request_id=request_id
        )
        
        raise HTTPException(
            status_code=403,
            detail=error_response.model_dump()
        )
    
    auth_service_url = GatewayConfig.AUTH_SERVICE_URL
    
    return {
        "message": "Use Auth Service directly for admin operations",
        "auth_service_url": f"{auth_service_url}/admin/users",
        "documentation": f"{auth_service_url}/docs",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway",
        "endpoint": "/admin/auth/users"
    } 