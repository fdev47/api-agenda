"""
Use case para exportar reservas a XLSX desde el API Gateway
"""
import logging
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.reservation.dto.requests.reservation_filter_request import ReservationFilterRequest

logger = logging.getLogger(__name__)


class ExportReservationsXlsxUseCase:
    """Use case para exportar reservas a XLSX usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, request: ReservationFilterRequest, access_token: str = "") -> bytes:
        """
        Exportar reservas a XLSX desde el reservation_service
        
        Args:
            request: DTO con los filtros de búsqueda
            access_token: Token de acceso para autenticación
            
        Returns:
            bytes: Contenido del archivo XLSX
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            # Construir parámetros de filtro (seguir el mismo patrón que list_reservations_use_case)
            params = {}
            
            # Filtros por usuario/cliente
            if request.user_id:
                params["user_id"] = request.user_id
            if request.customer_id:
                params["customer_id"] = request.customer_id
            
            # Filtros por sucursal
            if request.branch_id:
                params["branch_id"] = request.branch_id
            if request.branch_name:
                params["branch_name"] = request.branch_name
            if request.branch_code:
                params["branch_code"] = request.branch_code
            
            # Filtros por sector
            if request.sector_id:
                params["sector_id"] = request.sector_id
            if request.sector_name:
                params["sector_name"] = request.sector_name
            if request.sector_type_id:
                params["sector_type_id"] = request.sector_type_id
            
            # Filtros por cliente
            if request.customer_ruc:
                params["customer_ruc"] = request.customer_ruc
            if request.company_name:
                params["company_name"] = request.company_name
            
            # Filtros por fecha (mapear correctamente)
            if request.start_date:
                params["reservation_date_from"] = request.start_date
            if request.end_date:
                params["reservation_date_to"] = request.end_date
            
            # Filtros por estado (mapear correctamente)
            if request.status:
                params["reservation_status"] = request.status
            if request.status_list:
                params["reservation_status"] = ",".join(request.status_list)
            
            # Filtros por pedido
            if request.order_code:
                params["order_code"] = request.order_code
            
            # Filtros por tipo de carga
            if request.cargo_type:
                params["cargo_type"] = request.cargo_type
            
            async with APIClient(self.reservation_service_url, "") as client:
                xlsx_bytes = await client.get_bytes(
                    f"{config.API_PREFIX}/reservations/export/xlsx",
                    params=params,
                    headers=headers
                )
                return xlsx_bytes
                    
        except Exception as e:
            logger.error(f"❌ Error exportando reservas a XLSX: {str(e)}", exc_info=True)
            raise

