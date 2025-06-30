"""
Caso de uso para login de usuarios
"""
from ...domain.interfaces import IAuthProvider
from ...domain.entities import UserCredentials
from ...domain.dto.requests import LoginRequest
from ...domain.dto.responses import AuthResponse, TokenResponse, UserInfoResponse
from ...domain.exceptions import AuthError, AuthErrorCode


class LoginUserUseCase:
    """Caso de uso para login de usuarios"""
    
    def __init__(self, auth_provider: IAuthProvider):
        self._auth_provider = auth_provider
    
    def execute(self, request: LoginRequest) -> AuthResponse:
        """Ejecutar el caso de uso"""
        try:
            # Convertir request a entidad de dominio
            credentials = UserCredentials(
                email=request.email,
                password=request.password
            )
            
            # Autenticar usuario
            auth_token = self._auth_provider.authenticate_user(credentials)
            
            # Obtener información del usuario
            user = self._auth_provider.get_user_by_email(request.email)
            
            if not user:
                raise AuthError("Usuario no encontrado", AuthErrorCode.USER_NOT_FOUND.value)
            
            # Convertir a response DTOs
            token_response = TokenResponse(
                access_token=auth_token.access_token,
                refresh_token=auth_token.refresh_token,
                expires_at=auth_token.expires_at,
                token_type=auth_token.token_type
            )
            
            user_response = UserInfoResponse(
                user_id=user.user_id,
                email=user.email,
                display_name=user.display_name,
                phone_number=user.phone_number,
                email_verified=user.email_verified,
                custom_claims=user.custom_claims,
                created_at=user.created_at,
                last_sign_in=user.last_sign_in
            )
            
            return AuthResponse(token=token_response, user=user_response)
            
        except AuthError:
            raise
        except Exception as e:
            raise AuthError(f"Error en login: {str(e)}", AuthErrorCode.INVALID_CREDENTIALS.value) 