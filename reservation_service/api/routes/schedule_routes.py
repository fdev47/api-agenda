"""
Rutas para horarios
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import date
from typing import Optional
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
from ...domain.dto.responses.schedule_validation_responses import (
    ValidateScheduleDeletionResponse
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

# Configurar logging
logger = logging.getLogger(__name__)

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


@router.get("/available-slots", response_model=AvailableSlotsResponse)
async def get_available_slots(
    branch_id: int = Query(..., gt=0, description="ID de la sucursal"),
    schedule_date: date = Query(..., description="Fecha para consultar disponibilidad"),
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Obtener slots disponibles para una fecha específica"""
    logger.info(f"🚀 Endpoint get_available_slots llamado con branch_id: {branch_id}, schedule_date: {schedule_date}")
    
    try:
        logger.info("📝 Creando GetAvailableSlotsRequest...")
        # Crear el request object
        request = GetAvailableSlotsRequest(
            branch_id=branch_id,
            schedule_date=schedule_date
        )
        logger.info("✅ GetAvailableSlotsRequest creado correctamente")
        
        logger.info("📝 Obteniendo use case...")
        use_case = container.get_available_slots_use_case()
        logger.info("✅ Use case obtenido correctamente")
        
        logger.info("🔄 Ejecutando use case...")
        result = await use_case.execute(request)
        logger.info("✅ Use case ejecutado exitosamente")
        logger.info(f"📊 Resultado: {len(result.slots)} slots totales, {result.available_slots} disponibles")
        
        return result
    except (NoScheduleForDateException, PastDateException) as e:
        logger.warning(f"⚠️ Error de validación: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": e.error_code}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en get_available_slots: {str(e)}", exc_info=True)
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
        from ...domain.entities.day_of_week import DayOfWeek
        
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


# ===== ENDPOINTS DE VALIDACIÓN =====

@router.put("/{schedule_id}/update-with-validation", response_model=BranchScheduleResponse, status_code=status.HTTP_200_OK)
async def update_branch_schedule_with_validation(
    schedule_id: int,
    request: UpdateBranchScheduleRequest,
    auto_reschedule: bool = Query(False, description="Aplicar cambios automáticamente y reagendar reservas afectadas"),
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Actualizar un horario de sucursal con validación de reservas"""
    logger.info(f"🚀 Endpoint update_branch_schedule_with_validation llamado con schedule_id: {schedule_id}")
    logger.info(f"📝 Datos de actualización recibidos: {request}")
    logger.info(f"📝 Auto reschedule: {auto_reschedule}")
    
    try:
        logger.info("📝 Obteniendo use case...")
        use_case = container.update_branch_schedule_use_case()
        logger.info("✅ Use case obtenido correctamente")
        
        logger.info(f"🔄 Ejecutando actualización para schedule_id: {schedule_id}")
        result = await use_case.execute(schedule_id, request, auto_reschedule=auto_reschedule)
        logger.info("✅ Actualización completada exitosamente")
        logger.info(f"📊 Resultado: success={result.success}, message={result.message}")
        
        if result.success:
            logger.info("✅ Actualización exitosa, retornando horario actualizado")
            return result.schedule
        else:
            logger.warning(f"⚠️ Actualización requiere confirmación: {result.message}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": result.message,
                    "impact_analysis": result.impact_analysis.dict() if result.impact_analysis else None,
                    "requires_confirmation": result.requires_confirmation
                }
            )
            
    except ScheduleNotFoundException as e:
        logger.warning(f"⚠️ Horario no encontrado: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": e.error_code}
        )
    except (ScheduleOverlapException, InvalidScheduleTimeException, InvalidIntervalException) as e:
        logger.warning(f"⚠️ Error de validación: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": e.error_code}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en update_branch_schedule_with_validation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/{schedule_id}/validate-deletion", response_model=ValidateScheduleDeletionResponse, status_code=status.HTTP_200_OK)
async def validate_schedule_deletion(
    schedule_id: int,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Validar el impacto de eliminar un horario sin eliminarlo"""
    logger.info(f"🚀 Endpoint validate_schedule_deletion llamado con schedule_id: {schedule_id}")
    try:
        logger.info("📝 Obteniendo use case...")
        use_case = container.delete_branch_schedule_with_validation_use_case()
        logger.info("✅ Use case obtenido correctamente")
        
        logger.info(f"🔄 Ejecutando validación de eliminación para schedule_id: {schedule_id}")
        result = await use_case.validate_deletion(schedule_id)
        logger.info("✅ Validación de eliminación completada exitosamente")
        logger.info(f"📊 Resultado: can_delete={result.can_delete}, requires_rescheduling={result.requires_rescheduling}")
        
        logger.info("✅ Respuesta preparada exitosamente")
        return result
        
    except ScheduleNotFoundException as e:
        logger.warning(f"⚠️ Horario no encontrado: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": e.error_code}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en validate_schedule_deletion: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        ) 