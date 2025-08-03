"""
Rutas para rampas
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status, Path
from typing import List, Optional

from ...domain.dto.requests.create_ramp_request import CreateRampRequest
from ...domain.dto.requests.update_ramp_request import UpdateRampRequest
from ...domain.dto.requests.ramp_filter_request import RampFilterRequest
from ...domain.dto.responses.ramp_response import RampResponse
from ...domain.dto.responses.ramp_list_response import RampListResponse
from ...domain.exceptions.ramp_exceptions import (
    RampNotFoundException,
    RampAlreadyExistsException,
    RampValidationException
)
from ...infrastructure.container import container
from ..middleware import auth_middleware

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Ramps"])


def get_container():
    """Obtener el container de dependencias"""
    return container


@router.post("/", response_model=RampResponse, status_code=status.HTTP_201_CREATED)
async def create_ramp(
    request: CreateRampRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    container = Depends(get_container)
):
    """Crear una nueva rampa"""
    logger.info("🚀 Endpoint create_ramp llamado")
    
    try:
        use_case = container.create_ramp_use_case()
        result = await use_case.execute(request)
        logger.info("✅ Rampa creada exitosamente")
        return result
    except RampAlreadyExistsException as e:
        logger.warning(f"⚠️ Rampa ya existe: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message, "error_code": "RAMP_ALREADY_EXISTS"}
        )
    except RampValidationException as e:
        logger.error(f"❌ Error de validación: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": "VALIDATION_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en create_ramp: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/{ramp_id}", response_model=RampResponse)
async def get_ramp(
    ramp_id: int = Path(..., gt=0, description="ID de la rampa"),
    current_user=Depends(auth_middleware["require_auth"]),
    container = Depends(get_container)
):
    """Obtener una rampa por ID"""
    try:
        use_case = container.get_ramp_use_case()
        result = await use_case.execute(ramp_id)
        return result
    except RampNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RAMP_NOT_FOUND"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/", response_model=RampListResponse)
async def list_ramps(
    current_user=Depends(auth_middleware["require_auth"]),
    container = Depends(get_container),
    branch_id: Optional[int] = Query(None, gt=0, description="ID de la sucursal"),
    name: Optional[str] = Query(None, description="Nombre de la rampa"),
    is_available: Optional[bool] = Query(None, description="Disponibilidad de la rampa"),
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    sort_by: Optional[str] = Query(None, description="Campo para ordenar"),
    sort_order: Optional[str] = Query(None, description="Orden (asc/desc)")
):
    """Listar rampas con filtros"""
    try:
        request = RampFilterRequest(
            branch_id=branch_id,
            name=name,
            is_available=is_available,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        use_case = container.list_ramps_use_case()
        result = await use_case.execute(request)
        return result
    except Exception as e:
        logger.error(f"❌ Error inesperado en list_ramps: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.put("/{ramp_id}", response_model=RampResponse)
async def update_ramp(
    ramp_id: int = Path(..., gt=0, description="ID de la rampa"),
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    request: UpdateRampRequest = None
):
    """Actualizar una rampa"""
    try:
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Se requiere un body con los datos a actualizar", "error_code": "MISSING_REQUEST_BODY"}
            )
        
        use_case = container.update_ramp_use_case()
        result = await use_case.execute(ramp_id, request)
        return result
    except RampNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RAMP_NOT_FOUND"}
        )
    except RampValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": "VALIDATION_ERROR"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.delete("/{ramp_id}", response_model=RampResponse)
async def delete_ramp(
    ramp_id: int = Path(..., gt=0, description="ID de la rampa"),
    current_user=Depends(auth_middleware["require_auth"]),
    container = Depends(get_container)
):
    """Eliminar una rampa"""
    try:
        use_case = container.delete_ramp_use_case()
        result = await use_case.execute(ramp_id)
        return result
    except RampNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RAMP_NOT_FOUND"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


 