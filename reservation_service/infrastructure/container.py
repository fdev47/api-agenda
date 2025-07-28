# Container para dependencias del reservation_service
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession

from commons.database import get_db_session
from .repositories import ReservationRepositoryImpl, ScheduleRepositoryImpl
from ..application.use_cases import (
    # Casos de uso de horarios
    CreateBranchScheduleUseCase,
    GetBranchScheduleUseCase,
    ListBranchSchedulesUseCase,
    DeleteBranchScheduleUseCase,
    GetAvailableSlotsUseCase,
    ValidateScheduleChangesUseCase,
    UpdateBranchScheduleUseCase,
    DeleteBranchScheduleWithValidationUseCase,
    # Casos de uso de reservas
    CreateReservationUseCase,
    GetReservationUseCase,
    ListReservationsUseCase,
    UpdateReservationUseCase,
    DeleteReservationUseCase,
    ConfirmReservationUseCase,
    CancelReservationUseCase
)


class Container(containers.DeclarativeContainer):
    """Container de dependencias para el servicio de reservas"""
    
    # Configuración
    config = providers.Configuration()
    
    # Base de datos
    db_session = providers.Resource(get_db_session)
    
    # Repositorios
    reservation_repository = providers.Factory(
        ReservationRepositoryImpl,
        session=db_session
    )
    
    schedule_repository = providers.Factory(
        ScheduleRepositoryImpl
    )
    
    # Casos de uso de horarios
    create_branch_schedule_use_case = providers.Factory(
        CreateBranchScheduleUseCase,
        schedule_repository=schedule_repository
    )
    
    get_branch_schedule_use_case = providers.Factory(
        GetBranchScheduleUseCase,
        schedule_repository=schedule_repository
    )
    
    list_branch_schedules_use_case = providers.Factory(
        ListBranchSchedulesUseCase,
        schedule_repository=schedule_repository
    )
    
    delete_branch_schedule_use_case = providers.Factory(
        DeleteBranchScheduleUseCase,
        schedule_repository=schedule_repository
    )
    
    get_available_slots_use_case = providers.Factory(
        GetAvailableSlotsUseCase,
        schedule_repository=schedule_repository
    )
    
    # Casos de uso de validación de cambios
    validate_schedule_changes_use_case = providers.Factory(
        ValidateScheduleChangesUseCase,
        schedule_repository=schedule_repository,
        reservation_repository=reservation_repository
    )
    
    update_branch_schedule_use_case = providers.Factory(
        UpdateBranchScheduleUseCase,
        schedule_repository=schedule_repository,
        validate_changes_use_case=validate_schedule_changes_use_case
    )
    
    delete_branch_schedule_with_validation_use_case = providers.Factory(
        DeleteBranchScheduleWithValidationUseCase,
        schedule_repository=schedule_repository,
        validate_changes_use_case=validate_schedule_changes_use_case
    )
    
    # Casos de uso de reservas
    create_reservation_use_case = providers.Factory(
        CreateReservationUseCase,
        reservation_repository=reservation_repository
    )
    
    get_reservation_use_case = providers.Factory(
        GetReservationUseCase,
        reservation_repository=reservation_repository
    )
    
    list_reservations_use_case = providers.Factory(
        ListReservationsUseCase,
        reservation_repository=reservation_repository
    )
    
    update_reservation_use_case = providers.Factory(
        UpdateReservationUseCase,
        reservation_repository=reservation_repository
    )
    
    delete_reservation_use_case = providers.Factory(
        DeleteReservationUseCase,
        reservation_repository=reservation_repository
    )
    
    confirm_reservation_use_case = providers.Factory(
        ConfirmReservationUseCase,
        reservation_repository=reservation_repository
    )
    
    cancel_reservation_use_case = providers.Factory(
        CancelReservationUseCase,
        reservation_repository=reservation_repository
    )


# Instancia global del contenedor
container = Container()

__all__ = ["get_db_session"] 