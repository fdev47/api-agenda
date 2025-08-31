"""
Use case para listar reservas desde el API Gateway
"""
from typing import List, Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.reservation.dto.requests.reservation_filter_request import ReservationFilterRequest
from ....domain.reservation.dto.responses.reservation_list_response import ReservationListResponse
from ....domain.reservation.dto.responses.reservation_response import ReservationResponse


class ListReservationsUseCase:
    """Use case para listar reservas usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, request: ReservationFilterRequest, access_token: str = "") -> ReservationListResponse:
        """
        Listar reservas desde el reservation_service
        
        Args:
            request: DTO con los filtros de búsqueda
            access_token: Token de acceso para autenticación
            
        Returns:
            ReservationListResponse: Lista de reservas
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            # Construir parámetros de filtro (mapear correctamente a los parámetros del reservation_service)
            # El API Gateway usa skip/limit, pero el reservation_service espera page/limit
            page = (request.skip // request.limit) + 1 if request.limit > 0 else 1
            params = {
                "page": page,
                "limit": request.limit
            }
            
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
                params["status_list"] = ",".join(request.status_list)
            
            # Filtros por pedido
            if request.order_code:
                params["order_code"] = request.order_code
            
            # Filtros por tipo de carga
            if request.cargo_type:
                params["cargo_type"] = request.cargo_type
            
            # Ordenamiento (si el reservation_service los soporta)
            if request.sort_by:
                params["sort_by"] = request.sort_by
            if request.sort_order:
                params["sort_order"] = request.sort_order
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/reservations/",
                    params=params,
                    headers=headers
                )
                
                if response and "items" in response:
                    reservations = [ReservationResponse(**reservation) for reservation in response["items"]]
                    return ReservationListResponse(
                        reservations=reservations,
                        total=response.get("total", len(reservations)),
                        skip=request.skip,
                        limit=request.limit
                    )
                
                return ReservationListResponse(
                    reservations=[],
                    total=0,
                    skip=request.skip,
                    limit=request.limit
                )
                
        except Exception as e:
            return ReservationListResponse(
                reservations=[],
                total=0,
                skip=request.skip,
                limit=request.limit
            ) 