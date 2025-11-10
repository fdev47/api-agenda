"""
Rutas para rampas en el API Gateway
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header, Path
from typing import Optional
from datetime import datetime
from pydantic import ValidationError
from commons.error_codes import ErrorCode
from commons.api_client import HTTPError
from ...domain.ramp.dto.requests.create_ramp_request import CreateRampRequest
from ...domain.ramp.dto.requests.update_ramp_request import UpdateRampRequest
from ...domain.ramp.dto.requests.ramp_filter_request import RampFilterRequest
from ...domain.ramp.dto.responses.ramp_response import RampResponse
from ...domain.ramp.dto.responses.ramp_list_response import RampListResponse
from ...domain.ramp.dto.requests.ramp_slots_request import RampSlotsRequest
from ...domain.ramp.dto.responses.ramp_slots_response import RampSlotsResponse
from ...application.ramp.use_cases.create_ramp_use_case import CreateRampUseCase
from ...application.ramp.use_cases.get_ramp_use_case import GetRampUseCase
from ...application.ramp.use_cases.list_ramps_use_case import ListRampsUseCase
from ...application.ramp.use_cases.update_ramp_use_case import UpdateRampUseCase
from ...application.ramp.use_cases.delete_ramp_use_case import DeleteRampUseCase
from ...application.ramp.use_cases.get_ramp_slots_use_case import GetRampSlotsUseCase
from ..middleware import auth_middleware

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=RampResponse, status_code=status.HTTP_201_CREATED)
async def create_ramp(
    request: CreateRampRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Crear una nueva rampa"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = CreateRampUseCase()
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
        logger.error(f"❌ Error HTTP creando rampa: {str(e)}")
        
        # Intentar parsear el mensaje de error del location service
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
            detail={"message": error_message, "error_code": "LOCATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en create_ramp: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/slots", response_model=RampSlotsResponse, status_code=status.HTTP_200_OK)
async def get_ramp_slots(
    type: str = Query(..., description="Tipo de carga (SECO, FRIO, FLV)"),
    branch_id: int = Query(..., gt=0, description="ID de la sucursal"),
    schedule_date: str = Query(..., description="Fecha para consultar slots (YYYY-MM-DD)"),
    interval_time: int = Query(..., gt=0, description="Intervalo de tiempo en minutos para cada slot"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Obtener slots disponibles para rampas
    
    Args:
        type: Tipo de carga (SECO, FRIO, FLV)
        branch_id: ID de la sucursal
        schedule_date: Fecha en formato YYYY-MM-DD
        interval_time: Intervalo de tiempo en minutos para cada slot
        
    Returns:
        RampSlotsResponse con los slots disponibles
    """
    try:
        # Crear el request object desde los query parameters
        request = RampSlotsRequest(
            type=type,
            branch_id=branch_id,
            schedule_date=schedule_date,
            interval_time=interval_time
        )
        
        logger.info(f"📅 Obteniendo slots para tipo={request.type}, branch_id={request.branch_id}, fecha={request.schedule_date}, intervalo={request.interval_time}min")
        
        # Extraer access_token del header de autorización
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        
        use_case = GetRampSlotsUseCase()
        result = await use_case.execute(request, access_token)
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación de Pydantic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except ValueError as e:
        logger.warning(f"⚠️ Error de validación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado obteniendo slots: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/{ramp_id}", response_model=RampResponse)
async def get_ramp(
    ramp_id: int = Path(..., gt=0, description="ID de la rampa"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Obtener una rampa por ID"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = GetRampUseCase()
        result = await use_case.execute(ramp_id, access_token)
        return result
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP obteniendo rampa {ramp_id}: {str(e)}")
        
        # Intentar parsear el mensaje de error del location service
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
            detail={"message": error_message, "error_code": "LOCATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado obteniendo rampa {ramp_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/", response_model=RampListResponse)
async def list_ramps(
    branch_id: Optional[int] = Query(None, gt=0, description="ID de la sucursal"),
    name: Optional[str] = Query(None, description="Nombre de la rampa"),
    is_available: Optional[bool] = Query(None, description="Disponibilidad de la rampa"),
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    sort_by: Optional[str] = Query(None, description="Campo para ordenar"),
    sort_order: Optional[str] = Query(None, description="Orden (asc/desc)"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Listar rampas con filtros"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        
        request = RampFilterRequest(
            branch_id=branch_id,
            name=name,
            is_available=is_available,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        use_case = ListRampsUseCase()
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
        logger.error(f"❌ Error HTTP listando rampas: {str(e)}")
        
        # Intentar parsear el mensaje de error del location service
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
            detail={"message": error_message, "error_code": "LOCATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en list_ramps: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.put("/{ramp_id}", response_model=RampResponse)
async def update_ramp(
    ramp_id: int = Path(..., gt=0, description="ID de la rampa"),
    request: UpdateRampRequest = None,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Actualizar una rampa"""
    try:
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Se requiere un body con los datos a actualizar", "error_code": "MISSING_REQUEST_BODY"}
            )
        
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = UpdateRampUseCase()
        result = await use_case.execute(ramp_id, request, access_token)
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación de Pydantic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP actualizando rampa {ramp_id}: {str(e)}")
        
        # Intentar parsear el mensaje de error del location service
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
            detail={"message": error_message, "error_code": "LOCATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en update_ramp: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.delete("/{ramp_id}", response_model=RampResponse)
async def delete_ramp(
    ramp_id: int = Path(..., gt=0, description="ID de la rampa"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Eliminar una rampa"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = DeleteRampUseCase()
        result = await use_case.execute(ramp_id, access_token)
        return result
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP eliminando rampa {ramp_id}: {str(e)}")
        
        # Intentar parsear el mensaje de error del location service
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
            detail={"message": error_message, "error_code": "LOCATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en delete_ramp: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        ) 