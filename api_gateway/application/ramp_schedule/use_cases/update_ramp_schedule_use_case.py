"""
Caso de uso para actualizar un horario de rampa
"""
from commons.api_client import APIClient
from commons.config import config
from ....domain.ramp_schedule.dto.requests.ramp_schedule_requests import UpdateRampScheduleRequest
from ....domain.ramp_schedule.dto.responses.ramp_schedule_responses import RampScheduleUpdatedResponse


class UpdateRampScheduleUseCase:
    """Caso de uso para actualizar un horario de rampa"""
    
    def __init__(self):
        self.location_client = APIClient(base_url=config.LOCATION_SERVICE_URL)
    
    async def execute(self, schedule_id: int, request: UpdateRampScheduleRequest, access_token: str = "") -> RampScheduleUpdatedResponse:
        """Ejecutar el caso de uso"""
        
        # Preparar datos para el location_service
        payload = {}
        if request.day_of_week is not None:
            payload["day_of_week"] = request.day_of_week
        if request.name is not None:
            payload["name"] = request.name
        if request.start_time is not None:
            payload["start_time"] = request.start_time.strftime("%H:%M:%S")
        if request.end_time is not None:
            payload["end_time"] = request.end_time.strftime("%H:%M:%S")
        if request.is_active is not None:
            payload["is_active"] = request.is_active
        
        # Llamar al location_service
        async with self.location_client as client:
            response = await client.put(
                f"{config.API_PREFIX}/ramp-schedules/{schedule_id}",
                data=payload,
                headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
            )
        
        # Retornar respuesta
        return RampScheduleUpdatedResponse(**response)

