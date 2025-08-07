"""
Middleware de autenticación para uso en otros servicios
"""
import httpx
import os
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional, Union
from datetime import datetime
from dotenv import load_dotenv

from ..domain.dto.responses import AuthErrorResponse

# Cargar variables de entorno
load_dotenv()


class ExternalAuthMiddleware:
    """Middleware de autenticación para otros servicios"""
    
    def __init__(self, auth_service_url: str = None):
        """
        Inicializar middleware para otros servicios
        
        Args:
            auth_service_url: URL del servicio de autenticación
        """
        if auth_service_url is None:
            service_port = os.getenv("AUTH_SERVICE_PORT", "8001")
            auth_service_url = f"http://localhost:{service_port}"
        
        self.auth_service_url = auth_service_url
        self.security = HTTPBearer(auto_error=False)
    
    async def validate_token_with_service(self, token: str) -> dict:
        """
        Validar token llamando al servicio de autenticación
        
        Args:
            token: Token JWT a validar
            
        Returns:
            Dict con información del usuario si el token es válido
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.auth_service_url}/auth/validate-token",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("valid"):
                        return data.get("user")
                
                return None
                
        except Exception:
            return None
    
    async def get_current_user(
        self, 
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
    ) -> Optional[dict]:
        """Obtener usuario actual desde el token (opcional)"""
        if not credentials:
            return None
        
        user = await self.validate_token_with_service(credentials.credentials)
        return user
    
    async def require_auth(
        self, 
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> dict:
        """Requiere autenticación obligatoria"""
        user = await self.validate_token_with_service(credentials.credentials)
        
        if not user:
            error_response = AuthErrorResponse(
                error="auth_error",
                message="Token inválido o expirado",
                error_code="INVALID_TOKEN",
                token_expired=True,
                timestamp=datetime.now().isoformat()
            )
            
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=error_response.model_dump()
            )
        
        return user
    
    def require_role(self, required_role: str):
        """Decorator factory para requerir rol específico"""
        async def role_checker(current_user: dict = Depends(self.require_auth)):
            user_roles = current_user.get("custom_claims", {}).get("roles", [])
            if required_role not in user_roles:
                error_response = AuthErrorResponse(
                    error="auth_error",
                    message=f"Se requiere rol: {required_role}",
                    error_code="INSUFFICIENT_PERMISSIONS",
                    timestamp=datetime.now().isoformat()
                )
                
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content=error_response.model_dump()
                )
            return current_user
        return role_checker


# Función helper para crear middleware para otros servicios
def create_auth_middleware(auth_service_url: str = None) -> ExternalAuthMiddleware:
    """
    Crear middleware de autenticación para otros servicios
    
    Args:
        auth_service_url: URL del servicio de autenticación (opcional)
        
    Returns:
        ExternalAuthMiddleware configurado
    """
    
    return ExternalAuthMiddleware(auth_service_url) 