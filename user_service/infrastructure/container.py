"""
Contenedor de dependencias para el user_service
"""
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession
import os

from ..domain.interfaces.user_repository import UserRepository
from ..domain.interfaces.profile_repository import IProfileRepository
from ..domain.interfaces.role_repository import IRoleRepository

from ..data.repositories import (
    UserRepositoryImpl, ProfileRepositoryImpl, RoleRepositoryImpl
)

from ..application.use_cases import (
    CreateUserUseCase, UpdateUserUseCase, DeleteUserUseCase, ListUsersUseCase,
    CreateProfileUseCase, CreateRoleUseCase,
    # Nuevos casos de uso separados
    ActivateUserUseCase, DeactivateUserUseCase,
    GetUserByIdUseCase, GetUserByEmailUseCase, GetUserByAuthUidUseCase,
    # Casos de uso de administración
    AssignRoleUseCase, AssignPermissionUseCase, GetUserRolesUseCase
)

from .auth_service_client import AuthServiceClient


class UserServiceContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias para el user_service"""
    
    # Configuración
    config = providers.Configuration()
    
    # Base de datos
    db_session = providers.Singleton(AsyncSession)
    
    # Cliente de Auth Service
    auth_service_client = providers.Singleton(
        AuthServiceClient,
        base_url=os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    )
    
    # Repositorios
    user_repository = providers.Singleton(
        UserRepositoryImpl,
        session=db_session
    )
    
    profile_repository = providers.Singleton(
        ProfileRepositoryImpl,
        session=db_session
    )
    
    role_repository = providers.Singleton(
        RoleRepositoryImpl,
        session=db_session
    )
    
    # Casos de uso
    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        user_repository=user_repository,
        auth_service_client=auth_service_client
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
    
    create_profile_use_case = providers.Factory(
        CreateProfileUseCase,
        profile_repository=profile_repository,
        role_repository=role_repository
    )
    
    create_role_use_case = providers.Factory(
        CreateRoleUseCase,
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