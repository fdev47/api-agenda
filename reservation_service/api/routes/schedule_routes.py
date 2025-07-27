"""
Rutas para horarios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date
from ...domain.entities.day_of_week import DayOfWeek
from ...domain.dto.requests.schedule_requests import (
    CreateBranchScheduleRequest,
    UpdateBranchScheduleRequest,
    GetAvailableSlotsRequest,
    GetBranchSchedulesRequest
)
from ...domain.dto.responses.schedule_responses import (
    BranchScheduleResponse,
    AvailableSlotsResponse,
    BranchScheduleListResponse,
    CreateBranchScheduleResponse,
    UpdateBranchScheduleResponse,
    DeleteBranchScheduleResponse
)
from ...application.use_cases.create_branch_schedule_use_case import CreateBranchScheduleUseCase
from ...application.use_cases.update_branch_schedule_use_case import UpdateBranchScheduleUseCase
from ...application.use_cases.delete_branch_schedule_with_validation_use_case import DeleteBranchScheduleWithValidationUseCase
from ...application.use_cases.list_branch_schedules_use_case import ListBranchSchedulesUseCase
from ...application.use_cases.get_available_slots_use_case import GetAvailableSlotsUseCase
from ...domain.exceptions.schedule_exceptions import (
    ScheduleNotFoundException,
    ScheduleAlreadyExistsException,
    ScheduleOverlapException,
    InvalidScheduleTimeException,
    InvalidIntervalException,
    NoScheduleForDateException,
    PastDateException
)
from ...infrastructure.container import Container
from ..middleware import auth_middleware

router = APIRouter(prefix="/schedules", tags=["Schedules"])


def get_container() -> Container:
    """Obtener el container de dependencias"""
    return Container()


@router.post("/", response_model=CreateBranchScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_branch_schedule(
    request: CreateBranchScheduleRequest,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Crear un nuevo horario de sucursal"""
    try:
        use_case = container.create_branch_schedule_use_case()
        result = await use_case.execute(request)
        return result
    except ScheduleAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message, "error_code": e.error_code}
        )
    except (InvalidScheduleTimeException, InvalidIntervalException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": e.error_code}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/{schedule_id}", response_model=BranchScheduleResponse)
async def get_branch_schedule(
    schedule_id: int,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Obtener un horario de sucursal por ID"""
    try:
        use_case = container.get_branch_schedule_use_case()
        result = await use_case.execute(schedule_id)
        return result
    except ScheduleNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": e.error_code}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/branch/{branch_id}", response_model=BranchScheduleListResponse)
async def list_branch_schedules(
    branch_id: int,
    day_of_week: int = None,
    is_active: bool = None,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Listar horarios de una sucursal"""
    try:
        from ...domain.entities.schedule import DayOfWeek
        
        request = GetBranchSchedulesRequest(
            branch_id=branch_id,
            day_of_week=DayOfWeek(day_of_week) if day_of_week else None,
            is_active=is_active
        )
        
        use_case = container.list_branch_schedules_use_case()
        result = await use_case.execute(request)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Día de la semana inválido", "error_code": "INVALID_DAY_OF_WEEK"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.delete("/{schedule_id}", response_model=DeleteBranchScheduleResponse)
async def delete_branch_schedule(
    schedule_id: int,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Eliminar un horario de sucursal"""
    try:
        use_case = container.delete_branch_schedule_use_case()
        result = await use_case.execute(schedule_id)
        return result
    except ScheduleNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": e.error_code}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.post("/available-slots", response_model=AvailableSlotsResponse)
async def get_available_slots(
    request: GetAvailableSlotsRequest,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Obtener slots disponibles para una fecha específica"""
    try:
        use_case = container.get_available_slots_use_case()
        result = await use_case.execute(request)
        return result
    except (NoScheduleForDateException, PastDateException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": e.error_code}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        ) 