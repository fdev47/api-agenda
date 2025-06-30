"""
Caso de uso para validar tokens
"""
from ...domain.interfaces import IAuthProvider, ITokenValidator
from ...domain.dto.responses import UserInfoResponse
from ...domain.exceptions import AuthError, AuthErrorCode


class ValidateTokenUseCase:
    """Caso de uso para validar tokens"""
    
    def __init__(self, auth_provider: IAuthProvider, token_validator: ITokenValidator):
        self._auth_provider = auth_provider
        self._token_validator = token_validator
    
    def execute(self, token: str) -> UserInfoResponse:
        """Ejecutar el caso de uso"""
        try:
            # Validar formato básico
            if not self._token_validator.validate_token_format(token):
                raise AuthError("Formato de token inválido", AuthErrorCode.INVALID_TOKEN.value)
            
            # Verificar token con el proveedor
            user = self._auth_provider.verify_token(token)
            
            # Convertir a response DTO
            return UserInfoResponse(
                user_id=user.user_id,
                email=user.email,
                display_name=user.display_name,
                phone_number=user.phone_number,
                email_verified=user.email_verified,
                custom_claims=user.custom_claims,
                created_at=user.created_at,
                last_sign_in=user.last_sign_in
            )
            
        except AuthError:
            raise
        except Exception as e:
            raise AuthError(f"Error al validar token: {str(e)}", AuthErrorCode.INVALID_TOKEN.value) 