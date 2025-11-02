"""
Rutas para main_reservations en el API Gateway
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header, Path
from typing import Optional, List

from pydantic import ValidationError
from commons.error_codes import ErrorCode
from commons.api_client import HTTPError
from ...domain.reservation.dto.requests.create_main_reservation_request import CreateMainReservationRequest
from ...domain.reservation.dto.requests.update_main_reservation_request import UpdateMainReservationRequest
from ...domain.reservation.dto.responses.main_reservation_response import MainReservationResponse
from ...application.reservation.use_cases.create_main_reservation_use_case import CreateMainReservationUseCase
from ...application.reservation.use_cases.get_main_reservation_use_case import GetMainReservationUseCase
from ...application.reservation.use_cases.update_main_reservation_use_case import UpdateMainReservationUseCase
from ...application.reservation.use_cases.delete_main_reservation_use_case import DeleteMainReservationUseCase
from ..middleware import auth_middleware

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=MainReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_main_reservation(
    request: CreateMainReservationRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Crear una nueva main_reservation"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = CreateMainReservationUseCase()
        result = await use_case.execute(request, access_token)
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación de Pydantic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except HTTPError as e:
        logger.error(f"❌ Error HTTP creando main_reservation: {str(e)}")
        
        error_message = e.message
        try:
            import json
            error_data = json.loads(e.message)
            if isinstance(error_data, dict) and "message" in error_data:
                error_message = error_data["message"]
        except (json.JSONDecodeError, KeyError):
            pass
        
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": error_message, "error_code": "RESERVATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en create_main_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/{main_reservation_id}", response_model=MainReservationResponse)
async def get_main_reservation(
    main_reservation_id: int = Path(..., gt=0, description="ID de la main_reservation"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Obtener una main_reservation por ID"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = GetMainReservationUseCase()
        result = await use_case.execute(main_reservation_id, access_token)
        return result
    except HTTPError as e:
        logger.error(f"❌ Error HTTP obteniendo main_reservation {main_reservation_id}: {str(e)}")
        
        error_message = e.message
        try:
            import json
            error_data = json.loads(e.message)
            if isinstance(error_data, dict) and "message" in error_data:
                error_message = error_data["message"]
        except (json.JSONDecodeError, KeyError):
            pass
        
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": error_message, "error_code": "RESERVATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado obteniendo main_reservation {main_reservation_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/", response_model=List[MainReservationResponse])
async def list_main_reservations(
    sector_id: Optional[int] = Query(None, gt=0, description="Filtrar por sector_id"),
    reservation_id: Optional[int] = Query(None, gt=0, description="Filtrar por reservation_id"),
    reservation_date: Optional[str] = Query(None, description="Filtrar por fecha de reserva (YYYY-MM-DD)"),
    start_time: Optional[str] = Query(None, description="Filtrar por hora de inicio"),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Listar main_reservations con filtros opcionales"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        
        # Construir parámetros de query
        params = {}
        if sector_id:
            params["sector_id"] = sector_id
        if reservation_id:
            params["reservation_id"] = reservation_id
        if reservation_date:
            params["reservation_date"] = reservation_date
        if start_time:
            params["start_time"] = start_time
        params["skip"] = skip
        params["limit"] = limit
        
        headers = {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        # Llamar directamente al reservation_service
        from commons.api_client import APIClient
        from commons.config import config
        
        async with APIClient(config.RESERVATION_SERVICE_URL, "") as client:
            response = await client.get(
                f"{config.API_PREFIX}/main-reservations/",
                params=params,
                headers=headers
            )
            
            if response:
                return [MainReservationResponse(**item) for item in response]
            
            return []
            
    except HTTPError as e:
        logger.error(f"❌ Error HTTP listando main_reservations: {str(e)}")
        
        error_message = e.message
        try:
            import json
            error_data = json.loads(e.message)
            if isinstance(error_data, dict) and "message" in error_data:
                error_message = error_data["message"]
        except (json.JSONDecodeError, KeyError):
            pass
        
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": error_message, "error_code": "RESERVATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en list_main_reservations: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.put("/{main_reservation_id}", response_model=MainReservationResponse)
async def update_main_reservation(
    main_reservation_id: int = Path(..., gt=0, description="ID de la main_reservation"),
    request: UpdateMainReservationRequest = None,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Actualizar una main_reservation"""
    try:
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Se requiere un body con los datos a actualizar", "error_code": "MISSING_REQUEST_BODY"}
            )
        
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = UpdateMainReservationUseCase()
        result = await use_case.execute(request, access_token)
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación de Pydantic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except HTTPError as e:
        logger.error(f"❌ Error HTTP actualizando main_reservation {main_reservation_id}: {str(e)}")
        
        error_message = e.message
        try:
            import json
            error_data = json.loads(e.message)
            if isinstance(error_data, dict) and "message" in error_data:
                error_message = error_data["message"]
        except (json.JSONDecodeError, KeyError):
            pass
        
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": error_message, "error_code": "RESERVATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en update_main_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.delete("/{main_reservation_id}", response_model=MainReservationResponse, status_code=status.HTTP_200_OK)
async def delete_main_reservation(
    main_reservation_id: int = Path(..., gt=0, description="ID de la main_reservation"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Eliminar una main_reservation"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = DeleteMainReservationUseCase()
        result = await use_case.execute(main_reservation_id, access_token)
        return result
    except HTTPError as e:
        logger.error(f"❌ Error HTTP eliminando main_reservation {main_reservation_id}: {str(e)}")
        
        error_message = e.message
        try:
            import json
            error_data = json.loads(e.message)
            if isinstance(error_data, dict) and "message" in error_data:
                error_message = error_data["message"]
        except (json.JSONDecodeError, KeyError):
            pass
        
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": error_message, "error_code": "RESERVATION_SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en delete_main_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )

