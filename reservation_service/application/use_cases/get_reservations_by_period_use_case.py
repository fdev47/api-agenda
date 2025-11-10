"""
Use case para obtener reservas por período de tiempo
"""
import logging
from typing import List

from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.dto.requests.reservation_period_request import ReservationPeriodRequest
from ...domain.dto.responses.reservation_period_response import (
    ReservationPeriodResponse,
    ReservationPeriodItem
)

logger = logging.getLogger(__name__)


class GetReservationsByPeriodUseCase:
    """Use case para obtener reservas en un período específico"""
    
    def __init__(self, reservation_repository: ReservationRepository):
        """
        Inicializar use case
        
        Args:
            reservation_repository: Repositorio de reservas
        """
        self.reservation_repository = reservation_repository
    
    async def execute(self, request: ReservationPeriodRequest) -> ReservationPeriodResponse:
        """
        Ejecutar el use case
        
        Args:
            request: Request con parámetros de búsqueda
            
        Returns:
            ReservationPeriodResponse con lista de reservas
        """
        logger.info(f"🔍 Obteniendo reservas para sucursal {request.branch_id}")
        logger.info(f"📅 Período: {request.start_time} - {request.end_time}")
        if request.status:
            logger.info(f"📊 Filtrando por estado: {request.status}")
        
        # Obtener reservas del repositorio
        reservations = await self.reservation_repository.get_by_period(
            branch_id=request.branch_id,
            start_time=request.start_time,
            end_time=request.end_time,
            status=request.status
        )
        
        logger.info(f"✅ Se encontraron {len(reservations)} reservas")
        
        # Convertir a response items
        reservation_items: List[ReservationPeriodItem] = []
        for reservation in reservations:
            reservation_items.append(
                ReservationPeriodItem(
                    reservation_id=reservation.id,
                    start_time=reservation.start_time,
                    end_time=reservation.end_time
                )
            )
        
        return ReservationPeriodResponse(
            reservations=reservation_items,
            total=len(reservation_items)
        )

