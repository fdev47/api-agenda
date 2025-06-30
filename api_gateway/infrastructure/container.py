"""
Contenedor de dependencias para API Gateway
"""
from dependency_injector import containers, providers
import os

from .auth_service_client import AuthServiceClient
from .user_service_client import UserServiceClient
from ..application.use_cases import CreateUserUseCase


class APIGatewayContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias para API Gateway"""
    
    # Configuración
    config = providers.Configuration()
    
    # Clientes de servicios
    auth_service_client = providers.Singleton(
        AuthServiceClient,
        base_url=os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    )
    
    user_service_client = providers.Singleton(
        UserServiceClient,
        base_url=os.getenv("USER_SERVICE_URL", "http://localhost:8002")
    )
    
    # Use Cases de usuarios
    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        auth_service_client=auth_service_client,
        user_service_client=user_service_client
    )


# Instancia global del contenedor
container = APIGatewayContainer() 