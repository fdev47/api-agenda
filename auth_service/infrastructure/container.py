"""Dependency Injection Container"""

from typing import Optional
from auth_service.infrastructure.firebase import (
    FirebaseAuthProvider, FirebaseTokenValidator, FirebaseUserClaimsManager
)
from auth_service.use_cases.auth_use_cases import (
    CreateUserUseCase, ValidateTokenUseCase, ManageUserRolesUseCase
)
import os


class AuthServiceContainer:
    """Container para inyección de dependencias del servicio de auth"""
    
    def __init__(self, firebase_credentials_path: Optional[str] = None, project_id: Optional[str] = None):
        # Si no se proporciona project_id, intentar obtenerlo de variables de entorno
        if not project_id:
            project_id = (
                os.getenv('FIREBASE_PROJECT_ID') or 
                os.getenv('GOOGLE_CLOUD_PROJECT') or
                os.getenv('PROJECT_ID')
            )
        
        # Providers
        self._auth_provider = FirebaseAuthProvider(firebase_credentials_path, project_id)
        self._token_validator = FirebaseTokenValidator()
        self._claims_manager = FirebaseUserClaimsManager(self._auth_provider)
        
        # Use Cases
        self._create_user_use_case = CreateUserUseCase(
            self._auth_provider, self._claims_manager
        )
        self._validate_token_use_case = ValidateTokenUseCase(
            self._auth_provider, self._token_validator
        )
        self._manage_roles_use_case = ManageUserRolesUseCase(
            self._auth_provider, self._claims_manager
        )
    
    @property
    def auth_provider(self):
        return self._auth_provider
    
    @property
    def token_validator(self):
        return self._token_validator
    
    @property
    def claims_manager(self):
        return self._claims_manager
    
    @property
    def create_user_use_case(self):
        return self._create_user_use_case
    
    @property
    def validate_token_use_case(self):
        return self._validate_token_use_case
    
    @property
    def manage_roles_use_case(self):
        return self._manage_roles_use_case
