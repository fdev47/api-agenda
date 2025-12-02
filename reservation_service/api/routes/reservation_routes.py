"""
Rutas para reservas
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from typing import Optional
from datetime import datetime

from ...domain.dto.requests.create_reservation_request import CreateReservationRequest
from ...domain.dto.requests.update_reservation_request import UpdateReservationRequest
from ...domain.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.dto.requests.reject_reservation_request import RejectReservationRequest
from ...domain.dto.requests.complete_reservation_request import CompleteReservationRequest
from ...domain.dto.requests.reservation_period_request import ReservationPeriodRequest
from ...domain.dto.requests.export_reservations_request import ExportReservationsRequest
from ...domain.dto.responses.reservation_response import ReservationResponse
from ...domain.dto.responses.reservation_detail_response import ReservationDetailResponse
from ...domain.dto.responses.reservation_list_response import ReservationListResponse
from ...domain.dto.responses.reservation_summary_response import ReservationSummaryResponse
from ...domain.dto.responses.reservation_summary_list_response import ReservationSummaryListResponse
from ...domain.dto.responses.reservation_period_response import ReservationPeriodResponse
from ...domain.exceptions.reservation_exceptions import (
    ReservationNotFoundException,
    ReservationAlreadyExistsException,
    ReservationValidationException,
    ReservationConflictException,
    ReservationStatusException
)
from ...infrastructure.container import container, Container
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
    from ...infrastructure.repositories.main_reservation_repository_impl import MainReservationRepositoryImpl
    return ListReservationsUseCase(
        reservation_repository=ReservationRepositoryImpl(),
        main_reservation_repository=MainReservationRepositoryImpl()
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


@router.get("/period", response_model=ReservationPeriodResponse)
async def get_reservations_by_period(
    branch_id: int = Query(..., description="ID de la sucursal"),
    start_time: datetime = Query(..., description="Fecha y hora de inicio (YYYY-MM-DD HH:MM:SS)"),
    end_time: datetime = Query(..., description="Fecha y hora de fin (YYYY-MM-DD HH:MM:SS)"),
    status: Optional[str] = Query(None, description="Estado de las reservas (PENDING, CONFIRMED, COMPLETED, CANCELLED)"),
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """
    Obtener todas las reservas en un período de tiempo para una sucursal.
    
    Args:
        branch_id: ID de la sucursal
        start_time: Fecha y hora de inicio del período
        end_time: Fecha y hora de fin del período
        status: Estado opcional para filtrar las reservas
    
    Returns:
        ReservationPeriodResponse: Lista de reservas con start_time, end_time y reservation_id
    """
    try:
        logger.info(f"📅 GET /reservations/period - branch_id: {branch_id}, start_time: {start_time}, end_time: {end_time}, status: {status}")
        
        # Crear el request DTO
        request = ReservationPeriodRequest(
            branch_id=branch_id,
            start_time=start_time,
            end_time=end_time,
            status=status
        )
        
        # Obtener el use case del container
        use_case = container.get_reservations_by_period_use_case()
        
        # Ejecutar el use case
        result = await use_case.execute(request)
        
        logger.info(f"✅ Se obtuvieron {result.total} reservas en el período")
        return result
        
    except ValueError as e:
        logger.warning(f"⚠️ Datos de entrada inválidos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "error_code": "INVALID_INPUT"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en get_reservations_by_period: {str(e)}", exc_info=True)
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
    branch_code: Optional[str] = Query(None, description="Código de la sucursal"),
    
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
        from datetime import datetime
        
        # Convertir fechas si están presentes y no vacías
        date_from = None
        date_to = None
        
        def parse_date(date_str: str) -> datetime:
            """Función helper para parsear fechas en diferentes formatos"""
            if not date_str or not date_str.strip():
                return None
                
            date_str = date_str.strip()
            
            try:
                # Formato YYYY-MM-DD
                if len(date_str) == 10 and date_str.count('-') == 2:
                    return datetime.strptime(date_str, "%Y-%m-%d")
                
                # Formato YYYY-MM-DD HH:MM:SS
                elif len(date_str) == 19 and date_str.count('-') == 2 and date_str.count(':') == 2:
                    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                
                # Formato YYYY-MM-DDTHH:MM:SS (ISO sin zona horaria)
                elif 'T' in date_str and date_str.count(':') == 2:
                    # Remover la T y convertir a formato estándar
                    date_str_std = date_str.replace('T', ' ')
                    return datetime.strptime(date_str_std, "%Y-%m-%d %H:%M:%S")
                
                # Formato YYYY-MM-DDTHH:MM:SS.SSS (ISO con milisegundos)
                elif 'T' in date_str and '.' in date_str:
                    # Remover la T y convertir a formato estándar
                    date_str_std = date_str.replace('T', ' ')
                    return datetime.strptime(date_str_std, "%Y-%m-%d %H:%M:%S.%f")
                
                # Intentar formato ISO estándar
                else:
                    return datetime.fromisoformat(date_str)
                    
            except ValueError as e:
                raise ValueError(f"Formato de fecha inválido: {date_str}. Formatos soportados: YYYY-MM-DD, YYYY-MM-DD HH:MM:SS, YYYY-MM-DDTHH:MM:SS")
        
        # Parsear fechas
        if reservation_date_from:
            logger.info(f"🔍 Parseando fecha desde: {reservation_date_from}")
            date_from = parse_date(reservation_date_from)
            logger.info(f"✅ Fecha desde parseada: {date_from}")
        if reservation_date_to:
            logger.info(f"🔍 Parseando fecha hasta: {reservation_date_to}")
            date_to = parse_date(reservation_date_to)
            logger.info(f"✅ Fecha hasta parseada: {date_to}")
        
        request = ReservationFilterRequest(
            user_id=user_id,
            customer_id=customer_id,
            branch_id=branch_id,
            branch_name=branch_name,
            branch_code=branch_code,
            sector_id=sector_id,
            sector_name=sector_name,
            customer_name=company_name,  # Mapear company_name a customer_name (el repositorio usa customer_name para filtrar company_name)
            customer_email=None,
            reservation_date_from=date_from,
            reservation_date_to=date_to,
            status=reservation_status,
            order_code=order_code,
            cargo_type=cargo_type,
            page=page,
            limit=limit
        )
        
        use_case = get_list_reservations_use_case()
        result = await use_case.execute(request)
        
        return result
    except ValueError as e:
        logger.error(f"❌ Error de formato de fecha: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": str(e), 
                "error_code": "INVALID_DATE_FORMAT",
                "supported_formats": [
                    "YYYY-MM-DD",
                    "YYYY-MM-DD HH:MM:SS", 
                    "YYYY-MM-DDTHH:MM:SS",
                    "YYYY-MM-DDTHH:MM:SS.SSS"
                ]
            }
        )
    except Exception as e:
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




@router.get("/export/csv")
async def export_reservations_csv(
    # Filtros por usuario/cliente
    user_id: Optional[int] = Query(None, description="ID del usuario"),
    customer_id: Optional[int] = Query(None, description="ID del cliente"),
    
    # Filtros por sucursal
    branch_id: Optional[int] = Query(None, description="ID de la sucursal"),
    branch_name: Optional[str] = Query(None, description="Nombre de la sucursal"),
    branch_code: Optional[str] = Query(None, description="Código de la sucursal"),
    
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
    
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Exportar reservas a formato CSV"""
    try:
        request = ExportReservationsRequest(
            user_id=user_id,
            customer_id=customer_id,
            branch_id=branch_id,
            branch_name=branch_name,
            branch_code=branch_code,
            sector_id=sector_id,
            sector_name=sector_name,
            customer_ruc=customer_ruc,
            company_name=company_name,
            reservation_date_from=reservation_date_from,
            reservation_date_to=reservation_date_to,
            reservation_status=reservation_status,
            order_code=order_code,
            cargo_type=cargo_type
        )
        
        use_case = container.export_reservations_csv_use_case()
        csv_bytes = await use_case.execute(request)
        
        return Response(
            content=csv_bytes,
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": "attachment; filename=reservas.csv"
            }
        )
    except ValueError as e:
        logger.error(f"❌ Error de formato de fecha: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": str(e), 
                "error_code": "INVALID_DATE_FORMAT",
                "supported_formats": [
                    "YYYY-MM-DD",
                    "YYYY-MM-DD HH:MM:SS", 
                    "YYYY-MM-DDTHH:MM:SS",
                    "YYYY-MM-DDTHH:MM:SS.SSS"
                ]
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error al exportar reservas a CSV: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/export/xlsx")
async def export_reservations_xlsx(
    # Filtros por usuario/cliente
    user_id: Optional[int] = Query(None, description="ID del usuario"),
    customer_id: Optional[int] = Query(None, description="ID del cliente"),
    
    # Filtros por sucursal
    branch_id: Optional[int] = Query(None, description="ID de la sucursal"),
    branch_name: Optional[str] = Query(None, description="Nombre de la sucursal"),
    branch_code: Optional[str] = Query(None, description="Código de la sucursal"),
    
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
    
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Exportar reservas a formato XLSX"""
    try:
        request = ExportReservationsRequest(
            user_id=user_id,
            customer_id=customer_id,
            branch_id=branch_id,
            branch_name=branch_name,
            branch_code=branch_code,
            sector_id=sector_id,
            sector_name=sector_name,
            customer_ruc=customer_ruc,
            company_name=company_name,
            reservation_date_from=reservation_date_from,
            reservation_date_to=reservation_date_to,
            reservation_status=reservation_status,
            order_code=order_code,
            cargo_type=cargo_type
        )
        
        use_case = container.export_reservations_xlsx_use_case()
        xlsx_bytes = await use_case.execute(request)
        
        return Response(
            content=xlsx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=reservas.xlsx"
            }
        )
    except ValueError as e:
        logger.error(f"❌ Error de formato de fecha: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": str(e), 
                "error_code": "INVALID_DATE_FORMAT",
                "supported_formats": [
                    "YYYY-MM-DD",
                    "YYYY-MM-DD HH:MM:SS", 
                    "YYYY-MM-DDTHH:MM:SS",
                    "YYYY-MM-DDTHH:MM:SS.SSS"
                ]
            }
        )
    except ImportError as e:
        logger.error("❌ xlsxwriter no está instalado")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "xlsxwriter no está instalado. Ejecute: pip install xlsxwriter", "error_code": "MISSING_DEPENDENCY"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error al exportar reservas a XLSX: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


 