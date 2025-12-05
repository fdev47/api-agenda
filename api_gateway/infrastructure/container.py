"""
Container de dependencias para el API Gateway
"""
from dependency_injector import containers, providers
from ..application.user.use_cases import GetUserUseCase, GetUserByUsernameUseCase, ListUsersUseCase, CreateUserUseCase, UpdateUserUseCase, DeleteUserUseCase
from ..application.customer.use_cases import CreateCustomerUseCase, GetCustomerUseCase, GetCustomerByUsernameUseCase, ListCustomersUseCase, UpdateCustomerUseCase, DeleteCustomerUseCase
from ..application.schedule.use_cases.create_branch_schedule_use_case import CreateBranchScheduleUseCase
from ..application.schedule.use_cases.get_available_slots_use_case import GetAvailableSlotsUseCase
from ..application.schedule.use_cases.list_branch_schedules_use_case import ListBranchSchedulesUseCase
from ..application.schedule.use_cases.update_branch_schedule_use_case import UpdateBranchScheduleUseCase
from ..application.schedule.use_cases.delete_branch_schedule_with_validation_use_case import DeleteBranchScheduleWithValidationUseCase
from ..application.reservation.use_cases.create_reservation_use_case import CreateReservationUseCase
from ..application.reservation.use_cases.get_reservation_use_case import GetReservationUseCase
from ..application.reservation.use_cases.list_reservations_use_case import ListReservationsUseCase
from ..application.reservation.use_cases.update_reservation_use_case import UpdateReservationUseCase
from ..application.reservation.use_cases.cancel_reservation_use_case import CancelReservationUseCase

# Ramp Schedule
from ..application.ramp_schedule.use_cases.create_ramp_schedule_use_case import CreateRampScheduleUseCase
from ..application.ramp_schedule.use_cases.get_ramp_schedule_use_case import GetRampScheduleUseCase
from ..application.ramp_schedule.use_cases.list_ramp_schedules_use_case import ListRampSchedulesUseCase
from ..application.ramp_schedule.use_cases.update_ramp_schedule_use_case import UpdateRampScheduleUseCase
from ..application.ramp_schedule.use_cases.delete_ramp_schedule_use_case import DeleteRampScheduleUseCase
from ..application.ramp_schedule.use_cases.get_ramp_schedules_by_ramp_use_case import GetRampSchedulesByRampUseCase

# Auth
from ..application.auth.use_cases import (
    ChangePasswordUseCase,
    ChangePasswordByUsernameUserUseCase,
    ChangePasswordByUsernameCustomerUseCase
)


class Container(containers.DeclarativeContainer):
    """Container de dependencias para el API Gateway"""
    
    # Configuración
    config = providers.Configuration()
    
    # Use cases
    get_user_use_case = providers.Factory(GetUserUseCase)
    get_user_by_username_use_case = providers.Factory(GetUserByUsernameUseCase)
    list_users_use_case = providers.Factory(ListUsersUseCase)
    create_user_use_case = providers.Factory(CreateUserUseCase)
    update_user_use_case = providers.Factory(UpdateUserUseCase)
    delete_user_use_case = providers.Factory(DeleteUserUseCase)
    create_customer_use_case = providers.Factory(CreateCustomerUseCase)
    get_customer_use_case = providers.Factory(GetCustomerUseCase)
    get_customer_by_username_use_case = providers.Factory(GetCustomerByUsernameUseCase)
    list_customers_use_case = providers.Factory(ListCustomersUseCase)
    update_customer_use_case = providers.Factory(UpdateCustomerUseCase)
    delete_customer_use_case = providers.Factory(DeleteCustomerUseCase)
    create_branch_schedule_use_case = providers.Factory(CreateBranchScheduleUseCase)
    get_available_slots_use_case = providers.Factory(GetAvailableSlotsUseCase)
    list_branch_schedules_use_case = providers.Factory(ListBranchSchedulesUseCase)
    update_branch_schedule_use_case = providers.Factory(UpdateBranchScheduleUseCase)
    delete_branch_schedule_use_case = providers.Factory(DeleteBranchScheduleWithValidationUseCase)
    create_reservation_use_case = providers.Factory(CreateReservationUseCase)
    get_reservation_use_case = providers.Factory(GetReservationUseCase)
    list_reservations_use_case = providers.Factory(ListReservationsUseCase)
    update_reservation_use_case = providers.Factory(UpdateReservationUseCase)
    cancel_reservation_use_case = providers.Factory(CancelReservationUseCase)
    
    # Ramp Schedule
    create_ramp_schedule_use_case = providers.Factory(CreateRampScheduleUseCase)
    get_ramp_schedule_use_case = providers.Factory(GetRampScheduleUseCase)
    list_ramp_schedules_use_case = providers.Factory(ListRampSchedulesUseCase)
    update_ramp_schedule_use_case = providers.Factory(UpdateRampScheduleUseCase)
    delete_ramp_schedule_use_case = providers.Factory(DeleteRampScheduleUseCase)
    get_ramp_schedules_by_ramp_use_case = providers.Factory(GetRampSchedulesByRampUseCase)
    
    # Auth
    change_password_use_case = providers.Factory(ChangePasswordUseCase)
    change_password_by_username_user_use_case = providers.Factory(ChangePasswordByUsernameUserUseCase)
    change_password_by_username_customer_use_case = providers.Factory(ChangePasswordByUsernameCustomerUseCase) 