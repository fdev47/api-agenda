"""
Container de dependencias para el API Gateway
"""
from dependency_injector import containers, providers
from ..application.use_cases.user import GetUserUseCase, ListUsersUseCase, CreateUserUseCase


class Container(containers.DeclarativeContainer):
    """Container de dependencias para el API Gateway"""
    
    # Configuración
    config = providers.Configuration()
    
    # Use cases
    get_user_use_case = providers.Factory(GetUserUseCase)
    list_users_use_case = providers.Factory(ListUsersUseCase)
    create_user_use_case = providers.Factory(CreateUserUseCase) 