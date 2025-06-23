"""Authentication middleware"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from auth_service.domain.models import AuthenticatedUser, AuthError


class AuthMiddleware:
    """Middleware para autenticación"""
    
    def __init__(self, container):
        self.container = container
        self.security = HTTPBearer(auto_error=False)
    
    async def get_current_user(
        self, 
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
    ) -> Optional[AuthenticatedUser]:
        """Obtener usuario actual desde el token (opcional)"""
        if not credentials:
            return None
        
        try:
            user = self.container.validate_token_use_case.execute(credentials.credentials)
            return user
        except AuthError:
            return None
    
    async def require_auth(
        self, 
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> AuthenticatedUser:
        """Requiere autenticación obligatoria"""
        try:
            user = self.container.validate_token_use_case.execute(credentials.credentials)
            return user
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "unauthorized", "message": str(e)}
            )
    
    def require_role(self, required_role: str):
        """Decorator factory para requerir rol específico"""
        async def role_checker(current_user: AuthenticatedUser = Depends(self.require_auth)):
            user_roles = current_user.custom_claims.get('roles', [])
            if required_role not in user_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "error": "forbidden", 
                        "message": f"Se requiere rol: {required_role}"
                    }
                )
            return current_user
        return role_checker 