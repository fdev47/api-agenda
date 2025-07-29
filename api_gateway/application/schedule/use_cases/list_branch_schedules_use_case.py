"""
Use case para listar horarios de sucursal desde el API Gateway
"""
from typing import List, Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.schedule.dto.requests.schedule_requests import GetBranchSchedulesRequest
from ....domain.schedule.dto.responses.schedule_responses import BranchScheduleListResponse, BranchScheduleResponse


class ListBranchSchedulesUseCase:
    """Use case para listar horarios de sucursal usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, request: GetBranchSchedulesRequest, access_token: str = "") -> BranchScheduleListResponse:
        """
        Listar horarios de sucursal desde el reservation_service
        
        Args:
            request: DTO con los datos de la consulta
            access_token: Token de acceso para autenticación
            
        Returns:
            BranchScheduleListResponse: Respuesta con los horarios
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            params = {"branch_id": request.branch_id}
            if request.day_of_week:
                params["day_of_week"] = request.day_of_week.value
            if request.is_active is not None:
                params["is_active"] = request.is_active
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/schedules/branch/{request.branch_id}",
                    params=params,
                    headers=headers
                )
                
                if response and "schedules" in response:
                    schedules = [BranchScheduleResponse(**schedule) for schedule in response["schedules"]]
                    return BranchScheduleListResponse(
                        branch_id=response.get("branch_id", request.branch_id),
                        schedules=schedules,
                        total=response.get("total", len(schedules))
                    )
                
                return BranchScheduleListResponse(
                    branch_id=request.branch_id,
                    schedules=[],
                    total=0
                )
                
        except Exception as e:
            print(f"Error obteniendo horarios: {e}")
            return BranchScheduleListResponse(
                branch_id=request.branch_id,
                schedules=[],
                total=0
            ) 