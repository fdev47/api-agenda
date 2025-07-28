from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
import logging

from ...domain.dto.requests.schedule_requests import UpdateBranchScheduleRequest
from ...domain.dto.responses.schedule_responses import (
    BranchScheduleResponse
)
from ...domain.dto.responses.schedule_validation_responses import (
    ValidateScheduleDeletionResponse
)
from ...domain.exceptions.schedule_exceptions import (
    ScheduleNotFoundException,
    ScheduleAlreadyExistsException,
    ScheduleOverlapException,
    InvalidScheduleTimeException,
    InvalidIntervalException
)
from ...infrastructure.container import Container
from ..middleware import auth_middleware

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/schedules", tags=["Schedule Validation"])


def get_container() -> Container:
    """Obtener el container de dependencias"""
    return Container()


@router.put("/{schedule_id}", response_model=BranchScheduleResponse, status_code=status.HTTP_200_OK)
async def update_branch_schedule(
    schedule_id: int,
    request: UpdateBranchScheduleRequest,
    auto_reschedule: bool = Query(False, description="Aplicar cambios automáticamente y reagendar reservas afectadas"),
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Actualizar un horario de sucursal con validación de reservas"""
    logger.info(f"🚀 Endpoint update_branch_schedule llamado con schedule_id: {schedule_id}")
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
        logger.error(f"❌ Error inesperado en update_branch_schedule: {str(e)}", exc_info=True)
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