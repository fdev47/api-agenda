"""Firebase Token Validator implementation"""

from firebase_admin import auth as firebase_auth
from auth.domain.interfaces import ITokenValidator
from auth.domain.models import AuthError, AuthErrorCode


class FirebaseTokenValidator(ITokenValidator):
    """Validador de tokens específico para Firebase"""
    
    def validate_token_format(self, token: str) -> bool:
        try:
            parts = token.split('.')
            return len(parts) == 3
        except:
            return False
    
    def extract_user_id(self, token: str) -> str:
        try:
            decoded_token = firebase_auth.verify_id_token(token, check_revoked=False)
            return decoded_token['uid']
        except:
            raise AuthError(
                "No se puede extraer user_id del token", 
                AuthErrorCode.INVALID_TOKEN.value
            ) 