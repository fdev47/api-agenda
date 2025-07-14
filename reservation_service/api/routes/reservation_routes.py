from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from ...domain.dto.requests.reservation_requests import (
    CreateReservationRequest,
    UpdateReservationRequest,
    ReservationFilterRequest
)
from ...domain.dto.responses.reservation_responses import (
    ReservationResponse,
    ReservationListResponse,
    ReservationSummaryResponse,
    ReservationSummaryListResponse
)
from ...domain.exceptions.reservation_exceptions import (
    ReservationNotFoundException,
    ReservationAlreadyExistsException,
    ReservationValidationException,
    ReservationConflictException,
    ReservationStatusException
)
from ...infrastructure.container import Container

router = APIRouter(prefix="/reservations", tags=["Reservations"])


def get_container() -> Container:
    """Obtener el container de dependencias"""
    return Container()


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    request: CreateReservationRequest,
    container: Container = Depends(get_container)
):
    """Crear una nueva reserva"""
    try:
        use_case = container.create_reservation_use_case()
        result = await use_case.execute(request)
        return result
    except ReservationAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message, "error_code": "RESERVATION_ALREADY_EXISTS"}
        )
    except ReservationConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message, "error_code": "RESERVATION_CONFLICT"}
        )
    except ReservationValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "field_errors": e.field_errors, "error_code": "VALIDATION_ERROR"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation(
    reservation_id: int,
    container: Container = Depends(get_container)
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


@router.get("/", response_model=ReservationSummaryListResponse)
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
    status: Optional[str] = Query(None, description="Estado de la reserva"),
    
    # Filtros por pedido
    order_code: Optional[str] = Query(None, description="Código del pedido"),
    
    # Paginación
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(10, ge=1, le=100, description="Elementos por página"),
    
    container: Container = Depends(get_container)
):
    """Listar reservas con filtros y paginación"""
    try:
        from datetime import datetime
        
        # Convertir fechas si están presentes
        date_from = None
        date_to = None
        if reservation_date_from:
            date_from = datetime.fromisoformat(reservation_date_from)
        if reservation_date_to:
            date_to = datetime.fromisoformat(reservation_date_to)
        
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
            status=status,
            order_code=order_code,
            page=page,
            limit=limit
        )
        
        use_case = container.list_reservations_use_case()
        result = await use_case.execute(request)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Formato de fecha inválido", "error_code": "INVALID_DATE_FORMAT"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.put("/{reservation_id}", response_model=ReservationResponse)
async def update_reservation(
    reservation_id: int,
    request: UpdateReservationRequest,
    container: Container = Depends(get_container)
):
    """Actualizar una reserva existente"""
    try:
        use_case = container.update_reservation_use_case()
        result = await use_case.execute(reservation_id, request)
        return result
    except ReservationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RESERVATION_NOT_FOUND"}
        )
    except ReservationConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message, "error_code": "RESERVATION_CONFLICT"}
        )
    except ReservationValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "field_errors": e.field_errors, "error_code": "VALIDATION_ERROR"}
        )
    except ReservationStatusException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": "INVALID_STATUS"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: int,
    container: Container = Depends(get_container)
):
    """Eliminar una reserva"""
    try:
        use_case = container.delete_reservation_use_case()
        await use_case.execute(reservation_id)
        return None
    except ReservationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RESERVATION_NOT_FOUND"}
        )
    except ReservationStatusException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": "INVALID_STATUS"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.post("/{reservation_id}/confirm", response_model=ReservationResponse)
async def confirm_reservation(
    reservation_id: int,
    container: Container = Depends(get_container)
):
    """Confirmar una reserva"""
    try:
        use_case = container.confirm_reservation_use_case()
        result = await use_case.execute(reservation_id)
        return result
    except ReservationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RESERVATION_NOT_FOUND"}
        )
    except ReservationStatusException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": "INVALID_STATUS"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        )


@router.post("/{reservation_id}/cancel", response_model=ReservationResponse)
async def cancel_reservation(
    reservation_id: int,
    container: Container = Depends(get_container)
):
    """Cancelar una reserva"""
    try:
        use_case = container.cancel_reservation_use_case()
        result = await use_case.execute(reservation_id)
        return result
    except ReservationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "error_code": "RESERVATION_NOT_FOUND"}
        )
    except ReservationStatusException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "error_code": "INVALID_STATUS"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error interno del servidor", "error_code": "INTERNAL_ERROR"}
        ) 