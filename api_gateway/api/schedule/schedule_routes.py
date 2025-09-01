"""
Rutas para horarios en el API Gateway
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from datetime import date
from typing import Optional
from pydantic import ValidationError
from commons.error_codes import ErrorCode
from commons.api_client import HTTPError
from ...domain.schedule.dto.requests.schedule_requests import (
    CreateBranchScheduleRequest,
    UpdateBranchScheduleRequest,
    GetAvailableSlotsRequest,
    GetBranchSchedulesRequest,
    DayOfWeek
)
from ...domain.schedule.dto.responses.schedule_responses import (
    BranchScheduleResponse,
    AvailableSlotsResponse,
    BranchScheduleListResponse,
    CreateBranchScheduleResponse,
    UpdateBranchScheduleResponse,
    DeleteBranchScheduleResponse
)
from ...domain.schedule.dto.responses.schedule_validation_responses import (
    ValidateScheduleDeletionResponse
)
from ...application.schedule.use_cases.create_branch_schedule_use_case import CreateBranchScheduleUseCase
from ...application.schedule.use_cases.update_branch_schedule_use_case import UpdateBranchScheduleUseCase
from ...application.schedule.use_cases.delete_branch_schedule_with_validation_use_case import DeleteBranchScheduleWithValidationUseCase
from ...application.schedule.use_cases.list_branch_schedules_use_case import ListBranchSchedulesUseCase
from ...application.schedule.use_cases.get_available_slots_use_case import GetAvailableSlotsUseCase
from ..middleware import auth_middleware

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=CreateBranchScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_branch_schedule(
    request: CreateBranchScheduleRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Crear un nuevo horario de sucursal"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = CreateBranchScheduleUseCase()
        result = await use_case.execute(request, access_token)
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación de Pydantic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP creando horario: {str(e)}")
        
        # Intentar parsear el mensaje de error del reservation service
        error_message = e.message
        try:
            import json
            error_data = json.loads(e.message)
            if isinstance(error_data, dict) and "message" in error_data:
                error_message = error_data["message"]
        except (json.JSONDecodeError, KeyError):
            # Si no se puede parsear, usar el mensaje original
            pass
        
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": error_message, "error_code": "RESERVATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado creando horario: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/available-slots", response_model=AvailableSlotsResponse)
async def get_available_slots(
    branch_id: int = Query(..., gt=0, description="ID de la sucursal"),
    schedule_date: date = Query(..., description="Fecha para consultar disponibilidad"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Obtener slots disponibles para una fecha específica"""
    logger.info(f"🚀 Endpoint get_available_slots llamado con branch_id: {branch_id}, schedule_date: {schedule_date}")
    
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        
        logger.info("📝 Creando GetAvailableSlotsRequest...")
        request = GetAvailableSlotsRequest(
            branch_id=branch_id,
            schedule_date=schedule_date
        )
        logger.info("✅ GetAvailableSlotsRequest creado correctamente")
        
        logger.info("📝 Obteniendo use case...")
        use_case = GetAvailableSlotsUseCase()
        logger.info("✅ Use case obtenido correctamente")
        
        logger.info("🔄 Ejecutando use case...")
        result = await use_case.execute(request, access_token)
        logger.info("✅ Use case ejecutado exitosamente")
        logger.info(f"📊 Resultado: {len(result.slots)} slots totales, {result.available_slots} disponibles")
        
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación de Pydantic: {str(e)}")
        error_message = str(e)
        if "No se puede consultar disponibilidad para fechas pasadas" in error_message:
            error_code = ErrorCode.PAST_DATE.value
        else:
            error_code = ErrorCode.VALIDATION_ERROR.value
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": error_message, "error_code": error_code}
        )
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP obteniendo slots disponibles: {str(e)}")
        
        # Intentar parsear el mensaje de error del reservation service
        error_message = e.message
        try:
            import json
            error_data = json.loads(e.message)
            if isinstance(error_data, dict) and "message" in error_data:
                error_message = error_data["message"]
        except (json.JSONDecodeError, KeyError):
            # Si no se puede parsear, usar el mensaje original
            pass
        
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": error_message, "error_code": "RESERVATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en get_available_slots: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/branch/{branch_id}", response_model=BranchScheduleListResponse)
async def list_branch_schedules(
    branch_id: int,
    day_of_week: int = None,
    is_active: bool = None,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Listar horarios de una sucursal"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        
        request = GetBranchSchedulesRequest(
            branch_id=branch_id,
            day_of_week=DayOfWeek(day_of_week) if day_of_week else None,
            is_active=is_active
        )
        
        use_case = ListBranchSchedulesUseCase()
        result = await use_case.execute(request, access_token)
        
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Día de la semana inválido", "error_code": "INVALID_DAY_OF_WEEK"}
        )
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP listando horarios: {str(e)}")
        
        # Intentar parsear el mensaje de error del reservation service
        error_message = e.message
        try:
            import json
            error_data = json.loads(e.message)
            if isinstance(error_data, dict) and "message" in error_data:
                error_message = error_data["message"]
        except (json.JSONDecodeError, KeyError):
            # Si no se puede parsear, usar el mensaje original
            pass
        
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": error_message, "error_code": "RESERVATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado listando horarios: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.delete("/{schedule_id}", response_model=DeleteBranchScheduleResponse)
async def delete_branch_schedule(
    schedule_id: int,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Eliminar un horario de sucursal"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = DeleteBranchScheduleWithValidationUseCase()
        result = await use_case.execute(schedule_id, access_token)
        return result
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP eliminando horario {schedule_id}: {str(e)}")
        
        # Intentar parsear el mensaje de error del reservation service
        error_message = e.message
        try:
            import json
            error_data = json.loads(e.message)
            if isinstance(error_data, dict) and "message" in error_data:
                error_message = error_data["message"]
        except (json.JSONDecodeError, KeyError):
            # Si no se puede parsear, usar el mensaje original
            pass
        
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": error_message, "error_code": "RESERVATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado eliminando horario {schedule_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


# ===== ENDPOINTS DE VALIDACIÓN =====

@router.put("/{schedule_id}/update-with-validation", response_model=UpdateBranchScheduleResponse, status_code=status.HTTP_200_OK)
async def update_branch_schedule_with_validation(
    schedule_id: int,
    request: UpdateBranchScheduleRequest,
    auto_reschedule: bool = Query(False, description="Aplicar cambios automáticamente y reagendar reservas afectadas"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Actualizar un horario de sucursal con validación de reservas"""
    logger.info(f"🚀 Endpoint update_branch_schedule_with_validation llamado con schedule_id: {schedule_id}")
    logger.info(f"📝 Datos de actualización recibidos: {request}")
    logger.info(f"📝 Auto reschedule: {auto_reschedule}")
    
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        
        logger.info("📝 Obteniendo use case...")
        use_case = UpdateBranchScheduleUseCase()
        logger.info("✅ Use case obtenido correctamente")
        
        logger.info(f"🔄 Ejecutando actualización para schedule_id: {schedule_id}")
        result = await use_case.execute(schedule_id, request, access_token, auto_reschedule)
        logger.info("✅ Actualización completada exitosamente")
        logger.info(f"📊 Resultado: success={result.success}, message={result.message}")
        
        if result.success:
            logger.info("✅ Actualización exitosa, retornando respuesta completa")
            return result
        else:
            logger.warning(f"⚠️ Actualización requiere confirmación: {result.message}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": result.message,
                    "impact_analysis": result.impact_analysis,
                    "requires_confirmation": result.requires_confirmation
                }
            )
            
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación de Pydantic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP actualizando horario {schedule_id}: {str(e)}")
        
        # Intentar parsear el mensaje de error del reservation service
        error_message = e.message
        try:
            import json
            error_data = json.loads(e.message)
            if isinstance(error_data, dict) and "message" in error_data:
                error_message = error_data["message"]
        except (json.JSONDecodeError, KeyError):
            # Si no se puede parsear, usar el mensaje original
            pass
        
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": error_message, "error_code": "RESERVATION_SERVICE_ERROR"}
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
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Validar el impacto de eliminar un horario sin eliminarlo"""
    logger.info(f"🚀 Endpoint validate_schedule_deletion llamado con schedule_id: {schedule_id}")
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        
        logger.info("📝 Obteniendo use case...")
        use_case = DeleteBranchScheduleWithValidationUseCase()
        logger.info("✅ Use case obtenido correctamente")
        
        logger.info(f"🔄 Ejecutando validación de eliminación para schedule_id: {schedule_id}")
        result = await use_case.validate_deletion(schedule_id, access_token)
        logger.info("✅ Validación de eliminación completada exitosamente")
        logger.info(f"📊 Resultado: can_delete={result.can_delete}, requires_rescheduling={result.requires_rescheduling}")
        
        logger.info("✅ Respuesta preparada exitosamente")
        return result
        
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP validando eliminación de horario {schedule_id}: {str(e)}")
        
        # Intentar parsear el mensaje de error del reservation service
        error_message = e.message
        try:
            import json
            error_data = json.loads(e.message)
            if isinstance(error_data, dict) and "message" in error_data:
                error_message = error_data["message"]
        except (json.JSONDecodeError, KeyError):
            # Si no se puede parsear, usar el mensaje original
            pass
        
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": error_message, "error_code": "RESERVATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en validate_schedule_deletion: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        ) 