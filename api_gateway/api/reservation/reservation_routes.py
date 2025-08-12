"""
Rutas para reservas en el API Gateway
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header, Path
from typing import Optional, List
from datetime import datetime
from pydantic import ValidationError
from commons.error_codes import ErrorCode
from commons.api_client import HTTPError
from ...domain.reservation.dto.requests.create_reservation_request import CreateReservationRequest
from ...domain.reservation.dto.requests.update_reservation_request import UpdateReservationRequest
from ...domain.reservation.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.reservation.dto.requests.reject_reservation_request import RejectReservationRequest
from ...domain.reservation.dto.requests.complete_reservation_request import CompleteReservationRequest
from ...domain.reservation.dto.responses.reservation_response import ReservationResponse
from ...domain.reservation.dto.responses.reservation_detail_response import ReservationDetailResponse
from ...domain.reservation.dto.responses.reservation_list_response import ReservationListResponse
from ...domain.reservation.dto.responses.reservation_summary_response import ReservationSummaryResponse
from ...domain.reservation.dto.responses.reservation_summary_list_response import ReservationSummaryListResponse
from ...domain.reservation.dto.requests.available_ramp_request import AvailableRampRequest
from ...domain.reservation.dto.responses.available_ramp_response import AvailableRampResponse
from ...application.reservation.use_cases.create_reservation_use_case import CreateReservationUseCase
from ...application.reservation.use_cases.get_reservation_use_case import GetReservationUseCase
from ...application.reservation.use_cases.list_reservations_use_case import ListReservationsUseCase
from ...application.reservation.use_cases.update_reservation_use_case import UpdateReservationUseCase
from ...application.reservation.use_cases.cancel_reservation_use_case import CancelReservationUseCase
from ...application.reservation.use_cases.reject_reservation_use_case import RejectReservationUseCase
from ...application.reservation.use_cases.complete_reservation_use_case import CompleteReservationUseCase
from ...application.reservation.use_cases.get_available_ramp_use_case import GetAvailableRampUseCase
from ..middleware import auth_middleware

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    request: CreateReservationRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Crear una nueva reserva"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = CreateReservationUseCase()
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
        logger.error(f"❌ Error HTTP creando reserva: {str(e)}")
        
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
        logger.error(f"❌ Error inesperado en create_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/available-ramp", response_model=AvailableRampResponse)
async def get_available_ramp(
    branch_id: int = Query(..., gt=0, description="ID de la sucursal"),
    start_date: str = Query(..., description="Fecha y hora de inicio (YYYY-MM-DD HH:MM:SS)"),
    end_date: str = Query(..., description="Fecha y hora de fin (YYYY-MM-DD HH:MM:SS)"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Obtener una rampa disponible para una sucursal en un rango de fechas"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        
        # Crear el request con los parámetros de query
        request = AvailableRampRequest(
            branch_id=branch_id,
            start_date=start_date,
            end_date=end_date
        )
        
        use_case = GetAvailableRampUseCase()
        result = await use_case.execute(request, access_token)
        return result
    except ValueError as e:
        logger.warning(f"⚠️ Error de validación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": "VALIDATION_ERROR"}
        )
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP obteniendo rampa disponible: {str(e)}")
        
        # Intentar parsear el mensaje de error
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
            detail={"message": error_message, "error_code": "SERVICE_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en get_available_ramp: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/{reservation_id}", response_model=ReservationDetailResponse)
async def get_reservation(
    reservation_id: int = Path(..., gt=0, description="ID de la reserva"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Obtener una reserva por ID"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = GetReservationUseCase()
        result = await use_case.execute(reservation_id, access_token)
        return result
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP obteniendo reserva {reservation_id}: {str(e)}")
        
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
        logger.error(f"❌ Error inesperado obteniendo reserva {reservation_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/", response_model=ReservationListResponse)
async def list_reservations(
    user_id: Optional[int] = Query(None, gt=0, description="ID del usuario"),
    customer_id: Optional[int] = Query(None, gt=0, description="ID del cliente"),
    branch_id: Optional[int] = Query(None, gt=0, description="ID de la sucursal"),
    branch_name: Optional[str] = Query(None, description="Nombre de la sucursal"),
    branch_code: Optional[str] = Query(None, description="Código de la sucursal"),
    sector_id: Optional[int] = Query(None, gt=0, description="ID del sector"),
    sector_type_id: Optional[int] = Query(None, gt=0, description="ID del tipo de sector"),
    start_date: Optional[datetime] = Query(None, description="Fecha de inicio para filtrar"),
    end_date: Optional[datetime] = Query(None, description="Fecha de fin para filtrar"),
    status: Optional[str] = Query(None, description="Estado de la reserva"),
    status_list: Optional[str] = Query(None, description="Lista de estados separados por coma"),
    order_code: Optional[str] = Query(None, description="Código de pedido"),
    cargo_type: Optional[str] = Query(None, description="Tipo de carga"),
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    sort_by: Optional[str] = Query(None, description="Campo para ordenar"),
    sort_order: Optional[str] = Query(None, description="Orden (asc/desc)"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Listar reservas con filtros"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        
        # Procesar status_list
        status_list_parsed = None
        if status_list:
            status_list_parsed = [s.strip() for s in status_list.split(",")]
        
        request = ReservationFilterRequest(
            user_id=user_id,
            customer_id=customer_id,
            branch_id=branch_id,
            branch_name=branch_name,
            branch_code=branch_code,
            sector_id=sector_id,
            sector_type_id=sector_type_id,
            start_date=start_date,
            end_date=end_date,
            status=status,
            status_list=status_list_parsed,
            order_code=order_code,
            cargo_type=cargo_type,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        use_case = ListReservationsUseCase()
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
        logger.error(f"❌ Error HTTP listando reservas: {str(e)}")
        
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
        logger.error(f"❌ Error inesperado en list_reservations: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.put("/{reservation_id}", response_model=ReservationResponse)
async def update_reservation(
    reservation_id: int = Path(..., gt=0, description="ID de la reserva"),
    request: UpdateReservationRequest = None,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Actualizar una reserva"""
    try:
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Se requiere un body con los datos a actualizar", "error_code": "MISSING_REQUEST_BODY"}
            )
        
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = UpdateReservationUseCase()
        result = await use_case.execute(reservation_id, request, access_token)
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación de Pydantic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP actualizando reserva {reservation_id}: {str(e)}")
        
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
        logger.error(f"❌ Error inesperado en update_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.delete("/{reservation_id}", response_model=ReservationResponse)
async def cancel_reservation(
    reservation_id: int = Path(..., gt=0, description="ID de la reserva"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Cancelar una reserva"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = CancelReservationUseCase()
        result = await use_case.execute(reservation_id, access_token)
        return result
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP cancelando reserva {reservation_id}: {str(e)}")
        
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
        logger.error(f"❌ Error inesperado en cancel_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.post("/{reservation_id}/reject", response_model=ReservationResponse)
async def reject_reservation(
    request: RejectReservationRequest,
    reservation_id: int = Path(..., gt=0, description="ID de la reserva"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Rechazar una reserva con datos del rechazo"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = RejectReservationUseCase()
        result = await use_case.execute(reservation_id, request, access_token)
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación de Pydantic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP rechazando reserva {reservation_id}: {str(e)}")
        
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
        logger.error(f"❌ Error inesperado en reject_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.post("/{reservation_id}/completed", response_model=ReservationResponse)
async def complete_reservation(
    request: CompleteReservationRequest,
    reservation_id: int = Path(..., gt=0, description="ID de la reserva"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Completar una reserva con datos del completado"""
    try:
        access_token = authorization.replace("Bearer ", "") if authorization else ""
        use_case = CompleteReservationUseCase()
        result = await use_case.execute(reservation_id, request, access_token)
        return result
    except ValidationError as e:
        logger.warning(f"⚠️ Error de validación de Pydantic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": ErrorCode.VALIDATION_ERROR.value}
        )
    except HTTPError as e:
        # Propagar errores HTTP directamente
        logger.error(f"❌ Error HTTP completando reserva {reservation_id}: {str(e)}")
        
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
        logger.error(f"❌ Error inesperado en complete_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        ) 