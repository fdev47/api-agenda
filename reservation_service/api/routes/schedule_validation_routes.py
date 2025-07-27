from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from ...domain.dto.requests.schedule_requests import UpdateBranchScheduleRequest
from ...domain.dto.responses.schedule_responses import (
    BranchScheduleResponse,
    DeleteBranchScheduleResponse
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

router = APIRouter(prefix="/schedules", tags=["Schedule Validation"])


def get_container() -> Container:
    """Obtener el container de dependencias"""
    return Container()


@router.put("/{schedule_id}/validate", status_code=status.HTTP_200_OK)
async def validate_schedule_update(
    schedule_id: int,
    request: UpdateBranchScheduleRequest,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Validar el impacto de actualizar un horario sin aplicarlo"""
    try:
        use_case = container.update_branch_schedule_use_case()
        result = await use_case.execute(schedule_id, request, auto_reschedule=False)
        
        if result["success"]:
            return {
                "message": "Los cambios se pueden aplicar sin afectar reservas",
                "schedule": result["schedule"],
                "impact_analysis": result["impact_analysis"]
            }
        else:
            return {
                "message": result["message"],
                "requires_confirmation": True,
                "impact_analysis": result["impact_analysis"]
            }
            
    except ScheduleNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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


@router.put("/{schedule_id}", response_model=BranchScheduleResponse, status_code=status.HTTP_200_OK)
async def update_branch_schedule(
    schedule_id: int,
    request: UpdateBranchScheduleRequest,
    auto_reschedule: bool = Query(False, description="Aplicar cambios automáticamente y reagendar reservas afectadas"),
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Actualizar un horario de sucursal con validación de reservas"""
    try:
        use_case = container.update_branch_schedule_use_case()
        result = await use_case.execute(schedule_id, request, auto_reschedule=auto_reschedule)
        
        if result["success"]:
            return result["schedule"]
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": result["message"],
                    "impact_analysis": result["impact_analysis"],
                    "requires_confirmation": True
                }
            )
            
    except ScheduleNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": e.error_code}
        )
    except (ScheduleOverlapException, InvalidScheduleTimeException, InvalidIntervalException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": e.error_code}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/{schedule_id}/validate-deletion", status_code=status.HTTP_200_OK)
async def validate_schedule_deletion(
    schedule_id: int,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Validar el impacto de eliminar un horario sin eliminarlo"""
    try:
        use_case = container.delete_branch_schedule_with_validation_use_case()
        result = await use_case.validate_deletion(schedule_id)
        
        return {
            "message": "Análisis de impacto completado",
            "can_delete": result["can_delete"],
            "requires_rescheduling": result["requires_rescheduling"],
            "schedule_info": {
                "id": result["schedule_id"],
                "branch_id": result["branch_id"],
                "day_of_week": result["day_of_week"],
                "day_name": result["day_name"],
                "current_schedule": result["current_schedule"]
            },
            "impact_analysis": result["impact_analysis"]
        }
        
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


@router.delete("/{schedule_id}/with-validation", response_model=DeleteBranchScheduleResponse, status_code=status.HTTP_200_OK)
async def delete_branch_schedule_with_validation(
    schedule_id: int,
    auto_reschedule: bool = Query(False, description="Eliminar automáticamente y reagendar reservas afectadas"),
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Eliminar un horario de sucursal con validación de reservas"""
    try:
        use_case = container.delete_branch_schedule_with_validation_use_case()
        result = await use_case.execute(schedule_id, auto_reschedule=auto_reschedule)
        
        if result["success"]:
            return DeleteBranchScheduleResponse(
                id=result["schedule_id"],
                message=result["message"]
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": result["message"],
                    "impact_analysis": result["impact_analysis"],
                    "requires_confirmation": True
                }
            )
            
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