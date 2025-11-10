"""
Rutas de API para horarios de rampas en el API Gateway
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Header, status
from typing import Optional, List
from pydantic import ValidationError
from commons.error_codes import ErrorCode
from commons.api_client import HTTPError
from ...domain.ramp_schedule.dto.requests.ramp_schedule_requests import (
    CreateRampScheduleRequest,
    UpdateRampScheduleRequest,
    RampScheduleFilterRequest
)
from ...domain.ramp_schedule.dto.responses.ramp_schedule_responses import (
    RampScheduleResponse,
    RampScheduleCreatedResponse,
    RampScheduleUpdatedResponse,
    RampScheduleDeletedResponse,
    RampScheduleListResponse
)
from ...application.ramp_schedule.use_cases.create_ramp_schedule_use_case import CreateRampScheduleUseCase
from ...application.ramp_schedule.use_cases.get_ramp_schedule_use_case import GetRampScheduleUseCase
from ...application.ramp_schedule.use_cases.list_ramp_schedules_use_case import ListRampSchedulesUseCase
from ...application.ramp_schedule.use_cases.update_ramp_schedule_use_case import UpdateRampScheduleUseCase
from ...application.ramp_schedule.use_cases.delete_ramp_schedule_use_case import DeleteRampScheduleUseCase
from ...application.ramp_schedule.use_cases.get_ramp_schedules_by_ramp_use_case import GetRampSchedulesByRampUseCase
from ..middleware import auth_middleware

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=RampScheduleCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_ramp_schedule(
    request: CreateRampScheduleRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Crear un nuevo horario de rampa"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = CreateRampScheduleUseCase()
        result = await use_case.execute(request, access_token)
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except HTTPError as e:
        logger.error(f"❌ Error HTTP creando horario: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.message, "error_code": "LOCATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/ramp/{ramp_id}", response_model=List[RampScheduleResponse])
async def get_ramp_schedules_by_ramp(
    ramp_id: int = Path(..., gt=0, description="ID de la rampa"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Obtener todos los horarios de una rampa"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = GetRampSchedulesByRampUseCase()
        result = await use_case.execute(ramp_id, access_token)
        return result
    except HTTPError as e:
        logger.error(f"❌ Error HTTP obteniendo horarios de rampa {ramp_id}: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.message, "error_code": "LOCATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/{schedule_id}", response_model=RampScheduleResponse)
async def get_ramp_schedule(
    schedule_id: int = Path(..., gt=0, description="ID del horario"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Obtener un horario de rampa por ID"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = GetRampScheduleUseCase()
        result = await use_case.execute(schedule_id, access_token)
        return result
    except HTTPError as e:
        logger.error(f"❌ Error HTTP obteniendo horario {schedule_id}: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.message, "error_code": "LOCATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/", response_model=RampScheduleListResponse)
async def list_ramp_schedules(
    ramp_id: Optional[int] = Query(None, gt=0, description="Filtrar por rampa"),
    day_of_week: Optional[int] = Query(None, ge=1, le=7, description="Filtrar por día"),
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado"),
    limit: int = Query(100, ge=1, le=1000, description="Límite"),
    offset: int = Query(0, ge=0, description="Offset"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Listar horarios de rampas con filtros"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        
        filter_request = RampScheduleFilterRequest(
            ramp_id=ramp_id,
            day_of_week=day_of_week,
            name=name,
            is_active=is_active,
            limit=limit,
            offset=offset
        )
        
        use_case = ListRampSchedulesUseCase()
        result = await use_case.execute(filter_request, access_token)
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except HTTPError as e:
        logger.error(f"❌ Error HTTP listando horarios: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.message, "error_code": "LOCATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.put("/{schedule_id}", response_model=RampScheduleUpdatedResponse)
async def update_ramp_schedule(
    request: UpdateRampScheduleRequest,
    schedule_id: int = Path(..., gt=0, description="ID del horario"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Actualizar un horario de rampa"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = UpdateRampScheduleUseCase()
        result = await use_case.execute(schedule_id, request, access_token)
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except HTTPError as e:
        logger.error(f"❌ Error HTTP actualizando horario {schedule_id}: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.message, "error_code": "LOCATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.delete("/{schedule_id}", response_model=RampScheduleDeletedResponse)
async def delete_ramp_schedule(
    schedule_id: int = Path(..., gt=0, description="ID del horario"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Eliminar un horario de rampa"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = DeleteRampScheduleUseCase()
        result = await use_case.execute(schedule_id, access_token)
        return result
    except HTTPError as e:
        logger.error(f"❌ Error HTTP eliminando horario {schedule_id}: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.message, "error_code": "LOCATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )
