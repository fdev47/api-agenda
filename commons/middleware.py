"""
Middleware común para autenticación con debugging detallado
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
from datetime import datetime

from .auth_client import AuthClient, auth_dependencies
from .config import config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cliente de autenticación
auth_client = AuthClient(
    auth_service_url=config.AUTH_SERVICE_URL,
    timeout=config.AUTH_TIMEOUT
)


async def auth_middleware(request: Request, call_next):
    """
    Middleware de autenticación que valida tokens JWT
    """
    # Rutas que no requieren autenticación
    public_paths = {
        "/",
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/debug/openapi",
        "/debug/swagger-config",
        "/debug/test-auth"  # Para debugging
    }
    
    # Verificar si la ruta es pública
    if request.url.path in public_paths:
        return await call_next(request)
    
    # DEBUG: Mostrar todos los headers recibidos
    logger.info(f"=== DEBUG AUTH MIDDLEWARE ===")
    logger.info(f"Ruta: {request.url.path}")
    logger.info(f"Método: {request.method}")
    logger.info(f"Headers recibidos:")
    for header_name, header_value in request.headers.items():
        if header_name.lower() == 'authorization':
            logger.info(f"  {header_name}: {header_value[:20]}..." if len(header_value) > 20 else f"  {header_name}: {header_value}")
        else:
            logger.info(f"  {header_name}: {header_value}")
    
    # Obtener el token del header Authorization (case-insensitive)
    auth_header = None
    for header_name, header_value in request.headers.items():
        if header_name.lower() == 'authorization':
            auth_header = header_value
            break
    
    logger.info(f"Authorization header encontrado: {bool(auth_header)}")
    
    if not auth_header:
        logger.warning(f"Acceso denegado: No se proporcionó token de autorización - {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": True,
                "message": "Token de autorización requerido",
                "error_code": "AUTH_TOKEN_REQUIRED",
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path,
                "debug": {
                    "headers_present": list(request.headers.keys()),
                    "method": request.method,
                    "url": str(request.url)
                }
            }
        )
    
    # Validar formato del token
    if not auth_header.startswith("Bearer "):
        logger.warning(f"Acceso denegado: Formato de token inválido - {request.url.path}")
        logger.warning(f"Header recibido: '{auth_header}'")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": True,
                "message": "Formato de token inválido. Use 'Bearer <token>'",
                "error_code": "INVALID_TOKEN_FORMAT",
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path,
                "debug": {
                    "received_header": auth_header,
                    "expected_format": "Bearer <token>"
                }
            }
        )
    
    token = auth_header.split(" ")[1]
    logger.info(f"Token extraído (primeros 20 chars): {token[:20]}...")
    
    try:
        # Validar token con el servicio de autenticación
        logger.info(f"Validando token para ruta: {request.url.path}")
        user_data = await auth_client._validate_token(token)
        
        # Agregar información del usuario al request state
        request.state.user = user_data
        request.state.authenticated = True
        
        logger.info(f"Token válido para usuario: {user_data.get('user_id', 'unknown')}")
        return await call_next(request)
        
    except Exception as e:
        logger.error(f"Error validando token: {str(e)}")
        logger.error(f"Tipo de error: {type(e)}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": True,
                "message": "Token inválido o expirado",
                "error_code": "INVALID_TOKEN",
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path,
                "debug": {
                    "error_type": str(type(e)),
                    "error_message": str(e)
                }
            }
        )


def require_auth(request: Request) -> Dict[str, Any]:
    """
    Dependencia para requerir autenticación
    """
    if not hasattr(request.state, 'authenticated') or not request.state.authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticación requerida"
        )
    return request.state.user


def require_role(role: str):
    """
    Dependencia para requerir un rol específico
    """
    def role_checker(request: Request) -> Dict[str, Any]:
        user = require_auth(request)
        user_roles = user.get('roles', [])
        
        if role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Rol '{role}' requerido"
            )
        return user
    
    return role_checker


# Exportar middleware para uso en servicios
auth_middleware_dict = {
    "auth_middleware": auth_middleware,
    "require_auth": require_auth,           # Validación rápida (por defecto)
    "require_auth_full": auth_dependencies["require_auth_full"],  # Validación completa
    "require_role": require_role
}

# También exportar directamente para compatibilidad
__all__ = ["require_auth", "require_role", "require_auth_full", "auth_middleware_dict"]