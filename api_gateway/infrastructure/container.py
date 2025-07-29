"""
Container de dependencias para el API Gateway
"""
from dependency_injector import containers, providers
from ..application.user.use_cases import GetUserUseCase, ListUsersUseCase, CreateUserUseCase
from ..application.customer.use_cases.create_customer_use_case import CreateCustomerUseCase
from ..application.customer.use_cases.get_customer_use_case import GetCustomerUseCase
from ..application.customer.use_cases.list_customers_use_case import ListCustomersUseCase
from ..application.schedule.use_cases.create_branch_schedule_use_case import CreateBranchScheduleUseCase
from ..application.schedule.use_cases.get_available_slots_use_case import GetAvailableSlotsUseCase
from ..application.schedule.use_cases.list_branch_schedules_use_case import ListBranchSchedulesUseCase
from ..application.schedule.use_cases.update_branch_schedule_use_case import UpdateBranchScheduleUseCase
from ..application.schedule.use_cases.delete_branch_schedule_with_validation_use_case import DeleteBranchScheduleWithValidationUseCase


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
    create_branch_schedule_use_case = providers.Factory(CreateBranchScheduleUseCase)
    get_available_slots_use_case = providers.Factory(GetAvailableSlotsUseCase)
    list_branch_schedules_use_case = providers.Factory(ListBranchSchedulesUseCase)
    update_branch_schedule_use_case = providers.Factory(UpdateBranchScheduleUseCase)
    delete_branch_schedule_use_case = providers.Factory(DeleteBranchScheduleWithValidationUseCase) 