"""
Rutas de API para horarios de rampas
"""
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from typing import Optional, List
from ...infrastructure.container import Container
from ...domain.dto.requests.ramp_schedule_requests import (
    CreateRampScheduleRequest,
    UpdateRampScheduleRequest,
    RampScheduleFilterRequest
)
from ...domain.dto.responses.ramp_schedule_responses import (
    RampScheduleResponse,
    RampScheduleCreatedResponse,
    RampScheduleUpdatedResponse,
    RampScheduleDeletedResponse,
    RampScheduleListResponse
)
from ...domain.exceptions.ramp_schedule_exceptions import (
    RampScheduleNotFoundException,
    RampScheduleAlreadyExistsException
)
from ..middleware import auth_middleware

router = APIRouter()

# Obtener contenedor
def get_container():
    container = Container()
    return container


@router.post("/", response_model=RampScheduleCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_ramp_schedule(
    request: CreateRampScheduleRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    container = Depends(get_container)
):
    """Crear un nuevo horario de rampa"""
    try:
        use_case = container.create_ramp_schedule_use_case()
        result = await use_case.execute(request)
        return result
    except RampScheduleAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


# IMPORTANTE: Ruta específica ANTES de la genérica
@router.get("/ramp/{ramp_id}", response_model=List[RampScheduleResponse])
async def get_ramp_schedules_by_ramp(
    ramp_id: int = Path(..., gt=0, description="ID de la rampa"),
    current_user=Depends(auth_middleware["require_auth"]),
    container = Depends(get_container)
):
    """Obtener todos los horarios de una rampa"""
    try:
        use_case = container.get_ramp_schedules_by_ramp_use_case()
        result = await use_case.execute(ramp_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/{schedule_id}", response_model=RampScheduleResponse)
async def get_ramp_schedule(
    schedule_id: int = Path(..., gt=0, description="ID del horario"),
    current_user=Depends(auth_middleware["require_auth"]),
    container = Depends(get_container)
):
    """Obtener un horario de rampa por ID"""
    try:
        use_case = container.get_ramp_schedule_use_case()
        result = await use_case.execute(schedule_id)
        return result
    except RampScheduleNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/", response_model=RampScheduleListResponse)
async def list_ramp_schedules(
    current_user=Depends(auth_middleware["require_auth"]),
    container = Depends(get_container),
    ramp_id: Optional[int] = Query(None, gt=0, description="Filtrar por rampa"),
    day_of_week: Optional[int] = Query(None, ge=1, le=7, description="Filtrar por día de la semana (1=Lunes, 7=Domingo)"),
    name: Optional[str] = Query(None, description="Filtrar por nombre del horario"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación")
):
    """Listar horarios de rampas con filtros"""
    try:
        filter_request = RampScheduleFilterRequest(
            ramp_id=ramp_id,
            day_of_week=day_of_week,
            name=name,
            is_active=is_active,
            limit=limit,
            offset=offset
        )
        
        use_case = container.list_ramp_schedules_use_case()
        result = await use_case.execute(filter_request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.put("/{schedule_id}", response_model=RampScheduleUpdatedResponse)
async def update_ramp_schedule(
    request: UpdateRampScheduleRequest,
    schedule_id: int = Path(..., gt=0, description="ID del horario"),
    current_user=Depends(auth_middleware["require_auth"]),
    container = Depends(get_container)
):
    """Actualizar un horario de rampa"""
    try:
        use_case = container.update_ramp_schedule_use_case()
        result = await use_case.execute(schedule_id, request)
        return result
    except RampScheduleNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except RampScheduleAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete("/{schedule_id}", response_model=RampScheduleDeletedResponse)
async def delete_ramp_schedule(
    schedule_id: int = Path(..., gt=0, description="ID del horario"),
    current_user=Depends(auth_middleware["require_auth"]),
    container = Depends(get_container)
):
    """Eliminar un horario de rampa"""
    try:
        use_case = container.delete_ramp_schedule_use_case()
        result = await use_case.execute(schedule_id)
        return result
    except RampScheduleNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
