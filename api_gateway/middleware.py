"""
Middleware de autenticación para API Gateway
"""
import httpx
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional, Union
from datetime import datetime
import logging

from api_gateway.config import GatewayConfig
from api_gateway.domain.dto.responses import ErrorResponse

logger = logging.getLogger(__name__)


class GatewayAuthMiddleware:
    """Middleware de autenticación para API Gateway"""
    
    def __init__(self):
        self.security = HTTPBearer(auto_error=False)
        self.auth_service_url = GatewayConfig.AUTH_SERVICE_URL
        self.api_prefix = GatewayConfig.API_PREFIX
        self.timeout = 10.0  # 10 segundos timeout
    
    async def validate_token_with_service(self, token: str) -> dict:
        """
        Validar token llamando al Auth Service
        
        Args:
            token: Token JWT a validar
            
        Returns:
            Dict con información del usuario si el token es válido
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.auth_service_url}{self.api_prefix}/auth/validate-token"
                
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("valid"):
                        return data.get("user", {})
                    else:
                        return None
                else:
                    logger.error(f"Auth Service responded with status {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("Timeout al comunicarse con Auth Service")
            return None
        except httpx.RequestError as e:
            logger.error(f"Error de comunicación con Auth Service: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado al validar token: {str(e)}")
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
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> dict:
        """Requiere autenticación obligatoria"""
        user = await self.validate_token_with_service(credentials.credentials)
        
        if not user:
            # Obtener request_id si está disponible
            request_id = getattr(request.state, 'request_id', None)
            
            error_response = ErrorResponse(
                error="auth_error",
                message="Token inválido o expirado",
                error_code="INVALID_TOKEN",
                timestamp=datetime.now().isoformat(),
                request_id=request_id
            )
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response.model_dump()
            )
        
        return user
    
    def require_role(self, required_role: str):
        """Decorator factory para requerir rol específico"""
        async def role_checker(
            request: Request,
            current_user: dict = Depends(lambda: self.require_auth(request, None))
        ):
            user_roles = current_user.get("custom_claims", {}).get("roles", [])
            if required_role not in user_roles:
                # Obtener request_id si está disponible
                request_id = getattr(request.state, 'request_id', None)
                
                error_response = ErrorResponse(
                    error="auth_error",
                    message=f"Se requiere rol: {required_role}",
                    error_code="INSUFFICIENT_PERMISSIONS",
                    timestamp=datetime.now().isoformat(),
                    request_id=request_id
                )
                
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=error_response.model_dump()
                )
            return current_user
        return role_checker
    
    # Métodos de conveniencia para usar directamente en las rutas
    async def validate_auth(self, request: Request, authorization: Optional[str] = None) -> dict:
        """
        Validar autenticación desde una ruta
        """
        if not authorization or not authorization.startswith("Bearer "):
            # Obtener request_id si está disponible
            request_id = getattr(request.state, 'request_id', None)
            
            error_response = ErrorResponse(
                error="auth_error",
                message="Token no proporcionado o formato incorrecto",
                error_code="MISSING_TOKEN",
                timestamp=datetime.now().isoformat(),
                request_id=request_id
            )
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response.model_dump()
            )
        
        token = authorization.replace("Bearer ", "")
        user = await self.validate_token_with_service(token)
        
        if not user:
            # Obtener request_id si está disponible
            request_id = getattr(request.state, 'request_id', None)
            
            error_response = ErrorResponse(
                error="auth_error",
                message="Token inválido o expirado",
                error_code="INVALID_TOKEN",
                timestamp=datetime.now().isoformat(),
                request_id=request_id
            )
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response.model_dump()
            )
        
        return user


# Instancia global del middleware
auth_middleware = GatewayAuthMiddleware() 