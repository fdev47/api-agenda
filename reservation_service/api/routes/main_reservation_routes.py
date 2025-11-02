"""
Rutas para main_reservations
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from datetime import datetime

from ...domain.dto.requests.create_main_reservation_request import CreateMainReservationRequest
from ...domain.dto.requests.update_main_reservation_request import UpdateMainReservationRequest
from ...domain.dto.responses.main_reservation_response import MainReservationResponse
from ...domain.exceptions.reservation_exceptions import (
    ReservationNotFoundException,
    ReservationValidationException
)
from ...infrastructure.container import container
from ..middleware import auth_middleware

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/main-reservations", tags=["Main Reservations"])


def get_container():
    """Obtener el container de dependencias"""
    return container


@router.post("/", response_model=MainReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_main_reservation(
    request: CreateMainReservationRequest,
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Crear una nueva main_reservation"""
    logger.info("🚀 Endpoint create_main_reservation llamado")
    
    try:
        use_case = container.create_main_reservation_use_case()
        result = await use_case.execute(request)
        logger.info("✅ MainReservation creada exitosamente")
        return result
    except ReservationValidationException as e:
        logger.error(f"❌ Error de validación: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "field_errors": e.field_errors, "error_code": "VALIDATION_ERROR"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en create_main_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/{main_reservation_id}", response_model=MainReservationResponse)
async def get_main_reservation(
    main_reservation_id: int,
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Obtener una main_reservation por ID"""
    try:
        use_case = container.get_main_reservation_use_case()
        result = await use_case.execute(main_reservation_id)
        return result
    except ReservationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "MAIN_RESERVATION_NOT_FOUND"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en get_main_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/", response_model=List[MainReservationResponse])
async def list_main_reservations(
    sector_id: Optional[int] = Query(None, description="Filtrar por sector_id"),
    reservation_id: Optional[int] = Query(None, description="Filtrar por reservation_id"),
    reservation_date: Optional[str] = Query(None, description="Filtrar por fecha de reserva (YYYY-MM-DD)"),
    start_time: Optional[str] = Query(None, description="Filtrar por hora de inicio"),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Listar main_reservations con filtros opcionales"""
    logger.info("🚀 Endpoint list_main_reservations llamado")
    
    try:
        # Convertir strings de fecha a datetime si se proporcionan
        parsed_reservation_date = None
        if reservation_date:
            try:
                parsed_reservation_date = datetime.strptime(reservation_date, "%Y-%m-%d")
                logger.info(f"✅ Fecha de reserva parseada: {parsed_reservation_date}")
            except ValueError as e:
                logger.error(f"❌ Error de formato de fecha: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": "Formato de fecha inválido",
                        "error_code": "INVALID_DATE_FORMAT",
                        "supported_format": "YYYY-MM-DD"
                    }
                )
        
        parsed_start_time = None
        if start_time:
            try:
                parsed_start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                logger.info(f"✅ Hora de inicio parseada: {parsed_start_time}")
            except ValueError:
                # Intentar otros formatos comunes
                try:
                    parsed_start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    try:
                        parsed_start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f")
                    except ValueError as e:
                        logger.error(f"❌ Error de formato de hora: {str(e)}")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail={
                                "message": "Formato de hora inválido",
                                "error_code": "INVALID_TIME_FORMAT",
                                "supported_formats": [
                                    "YYYY-MM-DD HH:MM:SS",
                                    "YYYY-MM-DDTHH:MM:SS",
                                    "YYYY-MM-DDTHH:MM:SS.SSS"
                                ]
                            }
                        )
        
        # Obtener el repositorio desde el container
        repository = container.main_reservation_repository()
        
        # Llamar al método list del repositorio
        main_reservations, total = await repository.list(
            sector_id=sector_id,
            reservation_id=reservation_id,
            reservation_date=parsed_reservation_date,
            start_time=parsed_start_time,
            skip=skip,
            limit=limit
        )
        
        logger.info(f"✅ {len(main_reservations)} main_reservations encontradas de {total} totales")
        return main_reservations
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error inesperado en list_main_reservations: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.put("/{main_reservation_id}", response_model=MainReservationResponse)
async def update_main_reservation(
    main_reservation_id: int,
    request: UpdateMainReservationRequest,
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Actualizar una main_reservation existente"""
    logger.info(f"🚀 Endpoint update_main_reservation llamado con ID: {main_reservation_id}")
    
    try:
        # Verificar que el ID de la URL coincida con el del body
        if request.id != main_reservation_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "El ID de la URL no coincide con el del body", "error_code": "ID_MISMATCH"}
            )
        
        use_case = container.update_main_reservation_use_case()
        result = await use_case.execute(request)
        logger.info("✅ MainReservation actualizada exitosamente")
        return result
    except ReservationNotFoundException as e:
        logger.warning(f"⚠️ MainReservation no encontrada: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "MAIN_RESERVATION_NOT_FOUND"}
        )
    except ReservationValidationException as e:
        logger.warning(f"⚠️ Error de validación: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "field_errors": e.field_errors, "error_code": "VALIDATION_ERROR"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error inesperado en update_main_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.delete("/{main_reservation_id}", response_model=MainReservationResponse, status_code=status.HTTP_200_OK)
async def delete_main_reservation(
    main_reservation_id: int,
    container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Eliminar una main_reservation"""
    logger.info(f"🚀 Endpoint delete_main_reservation llamado con ID: {main_reservation_id}")
    
    try:
        use_case = container.delete_main_reservation_use_case()
        result = await use_case.execute(main_reservation_id)
        logger.info("✅ MainReservation eliminada exitosamente")
        return result
    except ReservationNotFoundException as e:
        logger.warning(f"⚠️ MainReservation no encontrada: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "MAIN_RESERVATION_NOT_FOUND"}
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado en delete_main_reservation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )

