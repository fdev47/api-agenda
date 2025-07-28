"""
Container de dependencias para el API Gateway
"""
from dependency_injector import containers, providers
from ..application.use_cases.user import GetUserUseCase, ListUsersUseCase, CreateUserUseCase
from ..application.use_cases.customer.create_customer_use_case import CreateCustomerUseCase
from ..application.use_cases.customer.get_customer_use_case import GetCustomerUseCase
from ..application.use_cases.customer.list_customers_use_case import ListCustomersUseCase


class Container(containers.DeclarativeContainer):
    """Container de dependencias para el API Gateway"""
    
    # Configuración
    config = providers.Configuration()
    
    # Use cases
    get_user_use_case = providers.Factory(GetUserUseCase)
    list_users_use_case = providers.Factory(ListUsersUseCase)
    create_user_use_case = providers.Factory(CreateUserUseCase)
    create_customer_use_case = providers.Factory(CreateCustomerUseCase)
    get_customer_use_case = providers.Factory(GetCustomerUseCase)
    list_customers_use_case = providers.Factory(ListCustomersUseCase) 