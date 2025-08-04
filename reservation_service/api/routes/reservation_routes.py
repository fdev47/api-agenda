"""
Rutas para reservas
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional

from ...domain.dto.requests.create_reservation_request import CreateReservationRequest
from ...domain.dto.requests.update_reservation_request import UpdateReservationRequest
from ...domain.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.dto.requests.reject_reservation_request import RejectReservationRequest
from ...domain.dto.requests.complete_reservation_request import CompleteReservationRequest
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.dto.responses.reservation_detail_response import ReservationDetailResponse
from ...domain.dto.responses.reservation_list_response import ReservationListResponse
from ...domain.dto.responses.reservation_summary_response import ReservationSummaryResponse
from ...domain.dto.responses.reservation_summary_list_response import ReservationSummaryListResponse
from ...domain.exceptions.reservation_exceptions import (
    ReservationNotFoundException,
    ReservationAlreadyExistsException,
    ReservationValidationException,
    ReservationConflictException,
    ReservationStatusException
)
from ...infrastructure.container import container
from ..middleware import auth_middleware
from ...application.use_cases.list_reservations_use_case import ListReservationsUseCase

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reservations", tags=["Reservations"])


def get_container():
    """Obtener el container de dependencias"""
    return container


def get_list_reservations_use_case():
    """Obtener el use case para listar reservas"""
    from ...infrastructure.repositories.reservation_repository_impl import ReservationRepositoryImpl
    return ListReservationsUseCase(
        reservation_repository=ReservationRepositoryImpl()
    )


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    request: CreateReservationRequest,
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Crear una nueva reserva"""
    logger.info("🚀 Endpoint create_reservation llamado")
    
    try:
        use_case = container.create_reservation_use_case()
        result = await use_case.execute(request)
        logger.info("✅ Reserva creada exitosamente")
        return result
    except ReservationAlreadyExistsException as e:
        logger.warning(f"⚠️ Conflicto de reserva: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message, "error_code": "RESERVATION_ALREADY_EXISTS"}
        )
    except ReservationConflictException as e:
        logger.warning(f"⚠️ Conflicto de reserva: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message, "error_code": "RESERVATION_CONFLICT"}
        )
    except ReservationValidationException as e:
        logger.error(f"❌ Error de validación: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "field_errors": e.field_errors, "error_code": "VALIDATION_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en create_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/{reservation_id}", response_model=ReservationDetailResponse)
async def get_reservation(
    reservation_id: int,
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Obtener una reserva por ID"""
    try:
        use_case = container.get_reservation_use_case()
        result = await use_case.execute(reservation_id)
        return result
    except ReservationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RESERVATION_NOT_FOUND"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/", response_model=ReservationListResponse)
async def list_reservations(
    # Filtros por usuario/cliente
    user_id: Optional[int] = Query(None, description="ID del usuario"),
    customer_id: Optional[int] = Query(None, description="ID del cliente"),
    
    # Filtros por sucursal
    branch_id: Optional[int] = Query(None, description="ID de la sucursal"),
    branch_name: Optional[str] = Query(None, description="Nombre de la sucursal"),
    
    # Filtros por sector
    sector_id: Optional[int] = Query(None, description="ID del sector"),
    sector_name: Optional[str] = Query(None, description="Nombre del sector"),
    
    # Filtros por cliente
    customer_ruc: Optional[str] = Query(None, description="RUC del cliente"),
    company_name: Optional[str] = Query(None, description="Nombre de la empresa"),
    
    # Filtros por fecha
    reservation_date_from: Optional[str] = Query(None, description="Fecha de reserva desde (YYYY-MM-DD)"),
    reservation_date_to: Optional[str] = Query(None, description="Fecha de reserva hasta (YYYY-MM-DD)"),
    
    # Filtros por estado
    reservation_status: Optional[str] = Query(None, description="Estado de la reserva"),
    
    # Filtros por pedido
    order_code: Optional[str] = Query(None, description="Código del pedido"),
    
    # Filtros por tipo de carga
    cargo_type: Optional[str] = Query(None, description="Tipo de carga"),
    
    # Paginación
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(10, ge=1, le=100, description="Elementos por página"),
    
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Listar reservas con filtros y paginación"""
    try:
        print(f"🔍 DEBUG: Iniciando list_reservations")
        print(f"🔍 DEBUG: Parámetros recibidos:")
        print(f"  - user_id: {user_id}")
        print(f"  - customer_id: {customer_id}")
        print(f"  - branch_id: {branch_id}")
        print(f"  - branch_name: {branch_name}")
        print(f"  - sector_id: {sector_id}")
        print(f"  - sector_name: {sector_name}")
        print(f"  - customer_ruc: {customer_ruc}")
        print(f"  - company_name: {company_name}")
        print(f"  - reservation_date_from: {reservation_date_from}")
        print(f"  - reservation_date_to: {reservation_date_to}")
        print(f"  - reservation_status: {reservation_status}")
        print(f"  - order_code: {order_code}")
        print(f"  - cargo_type: {cargo_type}")
        print(f"  - page: {page}")
        print(f"  - limit: {limit}")
        
        from datetime import datetime
        
        # Convertir fechas si están presentes y no vacías
        date_from = None
        date_to = None
        if reservation_date_from and reservation_date_from.strip():
            print(f"🔍 DEBUG: Procesando reservation_date_from: '{reservation_date_from}'")
            try:
                # Intentar diferentes formatos de fecha
                if len(reservation_date_from) == 10:  # YYYY-MM-DD
                    date_from = datetime.strptime(reservation_date_from, "%Y-%m-%d")
                elif len(reservation_date_from) == 19:  # YYYY-MM-DD HH:MM:SS
                    date_from = datetime.strptime(reservation_date_from, "%Y-%m-%d %H:%M:%S")
                else:
                    date_from = datetime.fromisoformat(reservation_date_from)
                print(f"🔍 DEBUG: date_from convertido: {date_from}")
            except ValueError as e:
                print(f"❌ ERROR: Formato de fecha inválido para reservation_date_from: {reservation_date_from}")
                raise ValueError(f"Formato de fecha inválido para reservation_date_from: {reservation_date_from}")
        if reservation_date_to and reservation_date_to.strip():
            print(f"🔍 DEBUG: Procesando reservation_date_to: '{reservation_date_to}'")
            try:
                # Intentar diferentes formatos de fecha
                if len(reservation_date_to) == 10:  # YYYY-MM-DD
                    date_to = datetime.strptime(reservation_date_to, "%Y-%m-%d")
                elif len(reservation_date_to) == 19:  # YYYY-MM-DD HH:MM:SS
                    date_to = datetime.strptime(reservation_date_to, "%Y-%m-%d %H:%M:%S")
                else:
                    date_to = datetime.fromisoformat(reservation_date_to)
                print(f"🔍 DEBUG: date_to convertido: {date_to}")
            except ValueError as e:
                print(f"❌ ERROR: Formato de fecha inválido para reservation_date_to: {reservation_date_to}")
                raise ValueError(f"Formato de fecha inválido para reservation_date_to: {reservation_date_to}")
        
        print(f"🔍 DEBUG: Creando ReservationFilterRequest")
        request = ReservationFilterRequest(
            user_id=user_id,
            customer_id=customer_id,
            branch_id=branch_id,
            branch_name=branch_name,
            sector_id=sector_id,
            sector_name=sector_name,
            customer_ruc=customer_ruc,
            company_name=company_name,
            reservation_date_from=date_from,
            reservation_date_to=date_to,
            status=reservation_status,
            order_code=order_code,
            cargo_type=cargo_type,
            page=page,
            limit=limit
        )
        print(f"🔍 DEBUG: ReservationFilterRequest creado exitosamente")
        
        print(f"🔍 DEBUG: Obteniendo use case")
        use_case = get_list_reservations_use_case()
        print(f"🔍 DEBUG: Use case obtenido: {use_case}")
        print(f"🔍 DEBUG: Tipo del use case: {type(use_case)}")
        print(f"🔍 DEBUG: Atributos del use case: {dir(use_case)}")
        print(f"🔍 DEBUG: Use case ejecutando...")
        result = await use_case.execute(request)
        print(f"🔍 DEBUG: Use case ejecutado exitosamente, resultado: {result}")
        return result
    except ValueError as e:
        print(f"❌ ERROR: ValueError en list_reservations: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Formato de fecha inválido", "error_code": "INVALID_DATE_FORMAT"}
        )
    except Exception as e:
        print(f"❌ ERROR: Excepción no manejada en list_reservations: {e}")
        print(f"❌ ERROR: Tipo de excepción: {type(e).__name__}")
        import traceback
        print(f"❌ ERROR: Traceback completo:")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.put("/{reservation_id}", response_model=ReservationResponse)
async def update_reservation(
    reservation_id: int,
    request: UpdateReservationRequest,
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Actualizar una reserva existente"""
    logger.info(f"🚀 Endpoint update_reservation llamado con ID: {reservation_id}")
    try:
        logger.info(f"📝 Datos de actualización recibidos: {request}")
        use_case = container.update_reservation_use_case()
        logger.info("✅ Use case obtenido correctamente")
        result = await use_case.execute(reservation_id, request)
        logger.info("✅ Reserva actualizada exitosamente")
        return result
    except ReservationNotFoundException as e:
        logger.warning(f"⚠️ Reserva no encontrada: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RESERVATION_NOT_FOUND"}
        )
    except ReservationConflictException as e:
        logger.warning(f"⚠️ Conflicto de reserva: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message, "error_code": "RESERVATION_CONFLICT"}
        )
    except ReservationValidationException as e:
        logger.warning(f"⚠️ Error de validación: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "field_errors": e.field_errors, "error_code": "VALIDATION_ERROR"}
        )
    except ReservationStatusException as e:
        logger.warning(f"⚠️ Estado de reserva inválido: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": "INVALID_STATUS"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en update_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.delete("/{reservation_id}", response_model=ReservationResponse, status_code=status.HTTP_200_OK)
async def delete_reservation(
    reservation_id: int,
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Eliminar una reserva"""
    logger.info(f"🚀 Endpoint delete_reservation llamado con ID: {reservation_id}")
    
    try:
        logger.info("📝 Obteniendo use case...")
        use_case = container.delete_reservation_use_case()
        logger.info("✅ Use case obtenido correctamente")
        
        logger.info(f"🔄 Ejecutando eliminación para reservation_id: {reservation_id}")
        result = await use_case.execute(reservation_id)
        logger.info("✅ Reserva eliminada exitosamente")
        
        return result
    except ReservationNotFoundException as e:
        logger.warning(f"⚠️ Reserva no encontrada: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RESERVATION_NOT_FOUND"}
        )
    except ReservationStatusException as e:
        logger.warning(f"⚠️ Estado de reserva inválido: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": "INVALID_STATUS"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en delete_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.post("/{reservation_id}/completed", response_model=ReservationResponse)
async def complete_reservation(
    reservation_id: int,
    request: CompleteReservationRequest,
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Completar una reserva"""
    logger.info(f"🚀 Endpoint complete_reservation llamado con ID: {reservation_id}")
    
    try:
        logger.info(f"📝 Datos de completado recibidos: {request}")
        use_case = container.complete_reservation_use_case()
        logger.info("✅ Use case obtenido correctamente")
        result = await use_case.execute(reservation_id, request)
        logger.info("✅ Reserva completada exitosamente")
        return result
    except ReservationNotFoundException as e:
        logger.warning(f"⚠️ Reserva no encontrada: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RESERVATION_NOT_FOUND"}
        )
    except ReservationStatusException as e:
        logger.warning(f"⚠️ Estado de reserva inválido: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": "INVALID_STATUS"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en complete_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.post("/{reservation_id}/cancel", response_model=ReservationResponse)
async def cancel_reservation(
    reservation_id: int,
    request: RejectReservationRequest,
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Cancelar/Rechazar una reserva"""
    logger.info(f"🚀 Endpoint cancel_reservation llamado con ID: {reservation_id}")
    
    try:
        logger.info(f"📝 Datos de cancelación/rechazo recibidos: {request}")
        use_case = container.reject_reservation_use_case()
        logger.info("✅ Use case obtenido correctamente")
        result = await use_case.execute(reservation_id, request)
        logger.info("✅ Reserva cancelada/rechazada exitosamente")
        return result
    except ReservationNotFoundException as e:
        logger.warning(f"⚠️ Reserva no encontrada: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RESERVATION_NOT_FOUND"}
        )
    except ReservationStatusException as e:
        logger.warning(f"⚠️ Estado de reserva inválido: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": "INVALID_STATUS"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en cancel_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


 