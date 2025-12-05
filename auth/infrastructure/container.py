"""
Contenedor de dependencias para el auth_service
"""
from dependency_injector import containers, providers

from ..domain.interfaces import IAuthProvider, ITokenValidator, IUserClaimsManager
from ..infrastructure.firebase.auth_provider import FirebaseAuthProvider
from ..infrastructure.firebase.token_validator import FirebaseTokenValidator
from ..infrastructure.firebase.claims_manager import FirebaseUserClaimsManager

from ..application.use_cases import (
    CreateUserUseCase, ValidateTokenUseCase, LoginUserUseCase, RefreshTokenUseCase,
    # Nuevos casos de uso separados
    AssignRoleUseCase, AssignPermissionUseCase, GetUserRolesUseCase,
    UpdateUserUseCase, DeleteUserUseCase, ChangePasswordUseCase, ChangePasswordByUserIdUseCase
)


class AuthServiceContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias para el auth_service"""
    
    # Configuración
    config = providers.Configuration()
    
    # Implementaciones de Firebase
    firebase_auth_provider = providers.Singleton(
        FirebaseAuthProvider
    )
    
    firebase_token_validator = providers.Singleton(
        FirebaseTokenValidator
    )
    
    firebase_claims_manager = providers.Singleton(
        FirebaseUserClaimsManager,
        auth_provider=firebase_auth_provider
    )
    
    # Interfaces (inyectadas con implementaciones concretas)
    auth_provider = providers.Singleton(
        FirebaseAuthProvider
    )
    
    token_validator = providers.Singleton(
        FirebaseTokenValidator
    )
    
    user_claims_manager = providers.Singleton(
        FirebaseUserClaimsManager,
        auth_provider=auth_provider
    )
    
    # Casos de uso
    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        auth_provider=auth_provider,
        claims_manager=user_claims_manager
    )
    
    login_user_use_case = providers.Factory(
        LoginUserUseCase,
        auth_provider=auth_provider
    )
    
    validate_token_use_case = providers.Factory(
        ValidateTokenUseCase,
        auth_provider=auth_provider,
        token_validator=token_validator
    )
    
    refresh_token_use_case = providers.Factory(
        RefreshTokenUseCase,
        auth_provider=auth_provider
    )
    
    # Nuevos casos de uso separados
    assign_role_use_case = providers.Factory(
        AssignRoleUseCase,
        auth_provider=auth_provider,
        claims_manager=user_claims_manager
    )
    
    assign_permission_use_case = providers.Factory(
        AssignPermissionUseCase,
        auth_provider=auth_provider,
        claims_manager=user_claims_manager
    )
    
    get_user_roles_use_case = providers.Factory(
        GetUserRolesUseCase,
        auth_provider=auth_provider,
        claims_manager=user_claims_manager
    )
    
    # Casos de uso para actualizar y eliminar usuarios
    update_user_use_case = providers.Factory(
        UpdateUserUseCase,
        auth_provider=auth_provider
    )
    
    delete_user_use_case = providers.Factory(
        DeleteUserUseCase,
        auth_provider=auth_provider
    )
    
    # Caso de uso para cambiar contraseña
    change_password_use_case = providers.Factory(
        ChangePasswordUseCase,
        auth_provider=auth_provider
    )
    
    # Caso de uso para cambiar contraseña por user_id
    change_password_by_user_id_use_case = providers.Factory(
        ChangePasswordByUserIdUseCase,
        auth_provider=auth_provider
    )


# Instancia global del contenedor
container = AuthServiceContainer()
