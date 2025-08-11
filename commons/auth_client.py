"""
Cliente de autenticación reutilizable para microservicios
Se comunica con Auth Service para validar tokens
"""
import httpx
from fastapi import Depends, HTTPException, Header
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

from commons.config import config

class AuthClient:
    """Cliente para comunicarse con Auth Service"""
    
    def __init__(self, auth_service_url: Optional[str] = None, api_prefix: Optional[str] = None, timeout: Optional[int] = None):
        self.auth_service_url = auth_service_url or config.AUTH_SERVICE_URL
        self.api_prefix = api_prefix or config.API_PREFIX
        self.timeout = timeout or config.AUTH_TIMEOUT
    
    async def _validate_token_quick(self, token: str) -> dict:
        """Validar token rápidamente con Auth Service (solo validez, sin datos completos)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.auth_service_url}{self.api_prefix}/auth/validate-token-quick",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("valid"):
                        # Para validación rápida, solo retornamos info básica del token
                        return {"valid": True, "message": "Token válido"}
                    else:
                        raise HTTPException(
                            status_code=401,
                            detail={
                                "error": "auth_error",
                                "message": data.get("message", "Token inválido"),
                                "error_code": "INVALID_TOKEN"
                            }
                        )
                else:
                    raise HTTPException(
                        status_code=401,
                        detail={
                            "error": "auth_error",
                            "message": "Error al validar token",
                            "error_code": "VALIDATION_ERROR"
                        }
                    )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "service_error",
                    "message": "Auth Service no disponible",
                    "error_code": "AUTH_SERVICE_TIMEOUT"
                }
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "service_error",
                    "message": f"Error de comunicación con Auth Service: {str(e)}",
                    "error_code": "AUTH_SERVICE_ERROR"
                }
            )

    async def _validate_token_full(self, token: str) -> dict:
        """Validar token completamente con Auth Service (incluye datos del usuario)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.auth_service_url}{self.api_prefix}/auth/validate-token",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("valid"):
                        return data.get("user", {})
                    else:
                        raise HTTPException(
                            status_code=401,
                            detail={
                                "error": "auth_error",
                                "message": data.get("message", "Token inválido"),
                                "error_code": "INVALID_TOKEN"
                            }
                        )
                else:
                    raise HTTPException(
                        status_code=401,
                        detail={
                            "error": "auth_error",
                            "message": "Error al validar token",
                            "error_code": "VALIDATION_ERROR"
                        }
                    )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "service_error",
                    "message": "Auth Service no disponible",
                    "error_code": "AUTH_SERVICE_TIMEOUT"
                }
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "service_error",
                    "message": f"Error de comunicación con Auth Service: {str(e)}",
                    "error_code": "AUTH_SERVICE_ERROR"
                }
            )

    async def _validate_token(self, token: str) -> dict:
        """Validar token con Auth Service (método por defecto - usa validación rápida)"""
        return await self._validate_token_quick(token)

def create_auth_dependencies(auth_service_url: Optional[str] = None, api_prefix: Optional[str] = None):
    """
    Factory para crear dependencias de autenticación
    
    Args:
        auth_service_url: URL del Auth Service (opcional, usa config por defecto)
        api_prefix: Prefijo de la API (opcional, usa config por defecto)
    
    Returns:
        Dict con las dependencias (require_auth, require_auth_full, require_role)
    """
    auth_client = AuthClient(auth_service_url, api_prefix)
    
    async def require_auth(authorization: Optional[str] = Header(None)) -> dict:
        """Requerir autenticación (validación rápida - solo verifica token)"""
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "auth_error",
                    "message": "Token de autorización requerido",
                    "error_code": "MISSING_TOKEN"
                }
            )
        
        token = authorization.replace("Bearer ", "")
        # Usar validación rápida por defecto
        result = await auth_client._validate_token_quick(token)
        return result
    
    async def require_auth_full(authorization: Optional[str] = Header(None)) -> dict:
        """Requerir autenticación completa (incluye datos del usuario)"""
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "auth_error",
                    "message": "Token de autorización requerido",
                    "error_code": "MISSING_TOKEN"
                }
            )
        
        token = authorization.replace("Bearer ", "")
        # Usar validación completa para obtener datos del usuario
        user = await auth_client._validate_token_full(token)
        return user
    
    def require_role(required_role: str):
        """Requerir rol específico - retorna una función dependency"""
        async def _require_role(authorization: Optional[str] = Header(None)) -> dict:
            user = await require_auth_full(authorization)  # Usar validación completa para roles
            
            # Verificar si el usuario tiene el rol requerido
            user_roles = user.get("custom_claims", {}).get("roles", [])
            if required_role not in user_roles:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "error": "auth_error",
                        "message": f"Rol '{required_role}' requerido",
                        "error_code": "INSUFFICIENT_PERMISSIONS"
                    }
                )
            
            return user
        
        return _require_role
    
    return {
        "require_auth": require_auth,           # Validación rápida (por defecto)
        "require_auth_full": require_auth_full, # Validación completa (para datos de usuario)
        "require_role": require_role            # Validación completa + verificación de rol
    }

# Instancia global para uso directo
auth_client = AuthClient()
auth_dependencies = create_auth_dependencies()

# Para compatibilidad hacia atrás
require_auth = auth_dependencies["require_auth"]
require_role = auth_dependencies["require_role"] 