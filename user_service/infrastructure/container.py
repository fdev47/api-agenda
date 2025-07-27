"""
Container de dependencias para el user_service
"""
import os
from dependency_injector import containers, providers
from commons.database import db_manager
from commons.auth_client import AuthClient
from ..data.repositories.profile_repository_impl import ProfileRepositoryImpl
from ..data.repositories.role_repository_impl import RoleRepositoryImpl
from ..data.repositories.user_repository_impl import UserRepositoryImpl
from ..application.use_cases import (
    CreateUserUseCase,
    GetUserByIdUseCase,
    GetUserByEmailUseCase,
    ListUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
    ActivateUserUseCase,
    DeactivateUserUseCase,
    CreateProfileUseCase,
    GetProfileByIdUseCase,
    ListProfilesUseCase,
    UpdateProfileUseCase,
    DeleteProfileUseCase,
    CreateRoleUseCase,
    GetRoleByIdUseCase,
    ListRolesUseCase,
    UpdateRoleUseCase,
    DeleteRoleUseCase,
    CreateCustomerUseCase,
    GetCustomerByIdUseCase,
    GetUserByAuthUidUseCase,
    GetCustomerByAuthUidUseCase,
    AssignRoleUseCase,
    AssignPermissionUseCase,
    GetUserRolesUseCase
)


class UserServiceContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias para el user_service"""
    
    # Configuración
    config = providers.Configuration()
    
    # Base de datos
    db_session = providers.Factory(
        lambda: db_manager.AsyncSessionLocal()
    )
    
    # Cliente de Auth Service
    auth_service_client = providers.Singleton(
        AuthClient,
        auth_service_url=os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    )
    
    # Repositorios
    user_repository = providers.Factory(
        UserRepositoryImpl,
        session=db_session
    )
    
    profile_repository = providers.Factory(
        ProfileRepositoryImpl,
        session=db_session
    )
    
    role_repository = providers.Factory(
        RoleRepositoryImpl,
        session=db_session
    )
    
    # Casos de uso
    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        user_repository=user_repository
    )
    
    # Casos de uso de obtención separados
    get_user_by_id_use_case = providers.Factory(
        GetUserByIdUseCase,
        user_repository=user_repository
    )
    
    get_user_by_email_use_case = providers.Factory(
        GetUserByEmailUseCase,
        user_repository=user_repository
    )
    
    get_user_by_auth_uid_use_case = providers.Factory(
        GetUserByAuthUidUseCase,
        user_repository=user_repository
    )
    
    update_user_use_case = providers.Factory(
        UpdateUserUseCase,
        user_repository=user_repository
    )
    
    delete_user_use_case = providers.Factory(
        DeleteUserUseCase,
        user_repository=user_repository
    )
    
    list_users_use_case = providers.Factory(
        ListUsersUseCase,
        user_repository=user_repository
    )
    
    # Casos de uso de gestión separados
    activate_user_use_case = providers.Factory(
        ActivateUserUseCase,
        user_repository=user_repository
    )
    
    deactivate_user_use_case = providers.Factory(
        DeactivateUserUseCase,
        user_repository=user_repository
    )
    
    # Casos de uso de Profile
    create_profile_use_case = providers.Factory(
        CreateProfileUseCase,
        profile_repository=profile_repository,
        role_repository=role_repository
    )
    
    get_profile_by_id_use_case = providers.Factory(
        GetProfileByIdUseCase,
        profile_repository=profile_repository
    )
    
    list_profiles_use_case = providers.Factory(
        ListProfilesUseCase,
        profile_repository=profile_repository
    )
    
    update_profile_use_case = providers.Factory(
        UpdateProfileUseCase,
        profile_repository=profile_repository
    )
    
    delete_profile_use_case = providers.Factory(
        DeleteProfileUseCase,
        profile_repository=profile_repository
    )
    
    # Casos de uso de Role
    create_role_use_case = providers.Factory(
        CreateRoleUseCase,
        role_repository=role_repository
    )
    
    get_role_by_id_use_case = providers.Factory(
        GetRoleByIdUseCase,
        role_repository=role_repository
    )
    
    list_roles_use_case = providers.Factory(
        ListRolesUseCase,
        role_repository=role_repository
    )
    
    update_role_use_case = providers.Factory(
        UpdateRoleUseCase,
        role_repository=role_repository
    )
    
    delete_role_use_case = providers.Factory(
        DeleteRoleUseCase,
        role_repository=role_repository
    )
    
    # Casos de uso de administración
    assign_role_use_case = providers.Factory(
        AssignRoleUseCase,
        user_repository=user_repository,
        role_repository=role_repository
    )
    
    assign_permission_use_case = providers.Factory(
        AssignPermissionUseCase,
        user_repository=user_repository
    )
    
    get_user_roles_use_case = providers.Factory(
        GetUserRolesUseCase,
        user_repository=user_repository,
        role_repository=role_repository
    )


# Instancia global del contenedor
container = UserServiceContainer() 