"""Firebase Auth Provider implementation"""

from typing import Optional
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from firebase_admin.exceptions import FirebaseError
from datetime import datetime
import os

from auth_service.domain.interfaces import IAuthProvider
from auth_service.domain.models import (
    UserRegistration, AuthenticatedUser, AuthToken, UserCredentials, 
    CustomClaims, AuthError, AuthErrorCode
)


class FirebaseAuthProvider(IAuthProvider):
    """Implementación concreta usando Firebase Auth"""
    
    def __init__(self, credentials_path: Optional[str] = None, project_id: Optional[str] = None):
        """
        Inicializar Firebase Admin SDK
        
        Args:
            credentials_path: Ruta al archivo de credenciales JSON
            project_id: ID del proyecto de Firebase (opcional si está en credenciales)
        """
        if not firebase_admin._apps:
            try:
                if credentials_path and os.path.exists(credentials_path):
                    # OPCIÓN 1: Usar archivo de credenciales
                    cred = credentials.Certificate(credentials_path)
                    
                    # Obtener project_id del archivo de credenciales si no se proporciona
                    if not project_id:
                        import json
                        with open(credentials_path, 'r') as f:
                            cred_data = json.load(f)
                            project_id = cred_data.get('project_id')
                    
                    firebase_admin.initialize_app(cred, {
                        'projectId': project_id
                    })
                    
                elif project_id:
                    # OPCIÓN 2: Solo con project_id (usando credenciales por defecto)
                    firebase_admin.initialize_app(options={
                        'projectId': project_id
                    })
                    
                else:
                    # OPCIÓN 3: Usar variables de entorno
                    project_id = os.getenv('GOOGLE_CLOUD_PROJECT') or os.getenv('FIREBASE_PROJECT_ID')
                    if not project_id:
                        raise ValueError(
                            "Se requiere project_id. Configúralo vía:\n"
                            "1. Parámetro project_id\n"
                            "2. Variable FIREBASE_PROJECT_ID\n" 
                            "3. Variable GOOGLE_CLOUD_PROJECT\n"
                            "4. Archivo de credenciales con project_id"
                        )
                    
                    firebase_admin.initialize_app(options={
                        'projectId': project_id
                    })
                    
            except Exception as e:
                raise ValueError(f"Error inicializando Firebase: {e}")
    
    def create_user(self, registration: UserRegistration) -> AuthenticatedUser:
        """Crear usuario en Firebase Auth"""
        try:
            user_record = firebase_auth.create_user(
                email=registration.email,
                password=registration.password,
                display_name=registration.display_name,
                phone_number=registration.phone_number,
                email_verified=False
            )
            return self._map_firebase_user_to_domain(user_record)
        except FirebaseError as e:
            raise self._map_firebase_error(e)
    
    def authenticate_user(self, credentials: UserCredentials) -> AuthToken:
        raise NotImplementedError("Se maneja en el cliente Firebase")
    
    def verify_token(self, token: str) -> AuthenticatedUser:
        try:
            decoded_token = firebase_auth.verify_id_token(token)
            user_record = firebase_auth.get_user(decoded_token['uid'])
            return self._map_firebase_user_to_domain(user_record)
        except FirebaseError as e:
            raise self._map_firebase_error(e)
    
    def refresh_token(self, refresh_token: str) -> AuthToken:
        raise NotImplementedError("Se maneja automáticamente en Firebase")
    
    def revoke_token(self, token: str) -> None:
        try:
            decoded_token = firebase_auth.verify_id_token(token)
            firebase_auth.revoke_refresh_tokens(decoded_token['uid'])
        except FirebaseError as e:
            raise self._map_firebase_error(e)
    
    def get_user_by_id(self, user_id: str) -> Optional[AuthenticatedUser]:
        try:
            user_record = firebase_auth.get_user(user_id)
            return self._map_firebase_user_to_domain(user_record)
        except firebase_auth.UserNotFoundError:
            return None
        except FirebaseError as e:
            raise self._map_firebase_error(e)
    
    def get_user_by_email(self, email: str) -> Optional[AuthenticatedUser]:
        try:
            user_record = firebase_auth.get_user_by_email(email)
            return self._map_firebase_user_to_domain(user_record)
        except firebase_auth.UserNotFoundError:
            return None
        except FirebaseError as e:
            raise self._map_firebase_error(e)
    
    def update_user_claims(self, user_id: str, claims: CustomClaims) -> None:
        try:
            custom_claims = {
                'roles': claims.roles,
                'permissions': claims.permissions,
                'organization_id': claims.organization_id
            }
            firebase_auth.set_custom_user_claims(user_id, custom_claims)
        except FirebaseError as e:
            raise self._map_firebase_error(e)
    
    def disable_user(self, user_id: str) -> None:
        try:
            firebase_auth.update_user(user_id, disabled=True)
        except FirebaseError as e:
            raise self._map_firebase_error(e)
    
    def delete_user(self, user_id: str) -> None:
        try:
            firebase_auth.delete_user(user_id)
        except FirebaseError as e:
            raise self._map_firebase_error(e)
    
    def _map_firebase_user_to_domain(self, user_record) -> AuthenticatedUser:
        return AuthenticatedUser(
            user_id=user_record.uid,
            email=user_record.email or "",
            display_name=user_record.display_name,
            phone_number=user_record.phone_number,
            email_verified=user_record.email_verified,
            custom_claims=user_record.custom_claims or {},
            created_at=datetime.fromtimestamp(
                user_record.user_metadata.creation_timestamp / 1000
            ),
            last_sign_in=datetime.fromtimestamp(
                user_record.user_metadata.last_sign_in_timestamp / 1000
            ) if user_record.user_metadata.last_sign_in_timestamp else None
        )
    
    def _map_firebase_error(self, firebase_error: FirebaseError) -> AuthError:
        error_mapping = {
            'EMAIL_ALREADY_EXISTS': AuthErrorCode.EMAIL_ALREADY_EXISTS,
            'WEAK_PASSWORD': AuthErrorCode.WEAK_PASSWORD,
            'USER_NOT_FOUND': AuthErrorCode.USER_NOT_FOUND,
            'INVALID_ID_TOKEN': AuthErrorCode.INVALID_TOKEN,
            'ID_TOKEN_EXPIRED': AuthErrorCode.TOKEN_EXPIRED,
            'USER_DISABLED': AuthErrorCode.USER_DISABLED,
        }
        
        error_code = error_mapping.get(firebase_error.code, None)
        return AuthError(
            str(firebase_error), 
            error_code.value if error_code else None
        )
