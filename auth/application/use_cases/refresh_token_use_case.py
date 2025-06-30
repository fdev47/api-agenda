"""
Caso de uso para refrescar tokens
"""
from ...domain.interfaces import IAuthProvider
from ...domain.dto.requests import RefreshTokenRequest
from ...domain.dto.responses import TokenResponse
from ...domain.exceptions import AuthError, AuthErrorCode


class RefreshTokenUseCase:
    """Caso de uso para refrescar tokens"""
    
    def __init__(self, auth_provider: IAuthProvider):
        self._auth_provider = auth_provider
    
    def execute(self, request: RefreshTokenRequest) -> TokenResponse:
        """Ejecutar el caso de uso"""
        try:
            # Refrescar token
            auth_token = self._auth_provider.refresh_token(request.refresh_token)
            
            # Convertir a response DTO
            return TokenResponse(
                access_token=auth_token.access_token,
                refresh_token=auth_token.refresh_token,
                expires_at=auth_token.expires_at,
                token_type=auth_token.token_type
            )
            
        except AuthError:
            raise
        except Exception as e:
            raise AuthError(f"Error al refrescar token: {str(e)}", AuthErrorCode.INVALID_TOKEN.value) 