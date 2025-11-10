"""
Caso de uso para listar horarios de rampas
"""
from commons.api_client import APIClient
from commons.config import config
from ....domain.ramp_schedule.dto.requests.ramp_schedule_requests import RampScheduleFilterRequest
from ....domain.ramp_schedule.dto.responses.ramp_schedule_responses import RampScheduleListResponse


class ListRampSchedulesUseCase:
    """Caso de uso para listar horarios de rampas"""
    
    def __init__(self):
        self.location_client = APIClient(base_url=config.LOCATION_SERVICE_URL)
    
    async def execute(self, filter_request: RampScheduleFilterRequest, access_token: str = "") -> RampScheduleListResponse:
        """Ejecutar el caso de uso"""
        
        # Preparar query parameters
        params = {}
        if filter_request.ramp_id is not None:
            params["ramp_id"] = filter_request.ramp_id
        if filter_request.day_of_week is not None:
            params["day_of_week"] = filter_request.day_of_week
        if filter_request.name is not None:
            params["name"] = filter_request.name
        if filter_request.is_active is not None:
            params["is_active"] = filter_request.is_active
        params["limit"] = filter_request.limit
        params["offset"] = filter_request.offset
        
        # Llamar al location_service
        async with self.location_client as client:
            response = await client.get(
                f"{config.API_PREFIX}/ramp-schedules",
                params=params,
                headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
            )
        
        # Retornar respuesta
        return RampScheduleListResponse(**response)

