"""Authentication middleware for internal and external services"""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional, Union
from datetime import datetime

from ..domain.entities import AuthenticatedUser
from ..domain.exceptions import AuthError, AuthErrorCode
from ..domain.dto.responses import AuthErrorResponse
from ..infrastructure.container import container


class AuthMiddleware:
    """Middleware para autenticación - Uso interno del servicio auth"""
    
    def __init__(self):
        self.security = HTTPBearer(auto_error=False)
    
    async def get_current_user(
        self, 
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
    ) -> Optional[AuthenticatedUser]:
        """Obtener usuario actual desde el token (opcional)"""
        if not credentials:
            return None
        
        try:
            user = container.validate_token_use_case.execute(credentials.credentials)
            return user
        except AuthError:
            return None
    
    async def require_auth(
        self, 
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> AuthenticatedUser:
        """Requiere autenticación obligatoria"""
        try:
            user = container.validate_token_use_case.execute(credentials.credentials)
            return user
        except AuthError as e:
            # Crear respuesta de error personalizada
            error_response = AuthErrorResponse(
                error="auth_error",
                message=str(e),
                error_code=e.error_code,
                token_expired=e.error_code == AuthErrorCode.TOKEN_EXPIRED.value,
                timestamp=datetime.now().isoformat()
            )
            
            # Determinar el código de estado HTTP apropiado
            status_code = status.HTTP_401_UNAUTHORIZED
            if e.error_code == AuthErrorCode.TOKEN_EXPIRED.value:
                status_code = status.HTTP_401_UNAUTHORIZED
            elif e.error_code == AuthErrorCode.USER_DISABLED.value:
                status_code = status.HTTP_403_FORBIDDEN
            elif e.error_code == AuthErrorCode.USER_NOT_FOUND.value:
                status_code = status.HTTP_404_NOT_FOUND
            
            # Usar HTTPException con el modelo de error personalizado
            raise HTTPException(
                status_code=status_code,
                detail=error_response.model_dump()
            )
    
    def require_role(self, required_role: str):
        """Decorator factory para requerir rol específico"""
        async def role_checker(current_user: AuthenticatedUser = Depends(self.require_auth)):
            user_roles = current_user.custom_claims.get('roles', [])
            if required_role not in user_roles:
                error_response = AuthErrorResponse(
                    error="auth_error",
                    message=f"Se requiere rol: {required_role}",
                    error_code="INSUFFICIENT_PERMISSIONS",
                    timestamp=datetime.now().isoformat()
                )
                
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=error_response.model_dump()
                )
            return current_user
        return role_checker


class TokenValidator:
    """Validador de tokens para uso en otros servicios"""
    
    def __init__(self, auth_service_url: str = None):
        """
        Inicializar validador de tokens
        
        Args:
            auth_service_url: URL del servicio de autenticación (opcional)
        """
        self.auth_service_url = auth_service_url or "http://localhost:8000"
    
    async def validate_token(self, token: str) -> Union[AuthenticatedUser, None]:
        """
        Validar token y retornar información del usuario
        
        Args:
            token: Token JWT a validar
            
        Returns:
            AuthenticatedUser si el token es válido, None si no lo es
        """
        try:
            # Usar el caso de uso de validación
            user = container.validate_token_use_case.execute(token)
            return user
        except AuthError:
            return None
    
    async def get_user_info(self, token: str) -> dict:
        """
        Obtener información del usuario desde el token
        
        Args:
            token: Token JWT
            
        Returns:
            Dict con información del usuario
        """
        user = await self.validate_token(token)
        if user:
            return {
                "user_id": user.user_id,
                "email": user.email,
                "display_name": user.display_name,
                "email_verified": user.email_verified,
                "custom_claims": user.custom_claims,
                "created_at": user.created_at.isoformat(),
                "last_sign_in": user.last_sign_in.isoformat() if user.last_sign_in else None
            }
        return None


# Instancia global del middleware para uso interno
auth_middleware = AuthMiddleware()

# Instancia global del validador para uso externo
token_validator = TokenValidator() 