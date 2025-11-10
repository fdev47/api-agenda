"""
Caso de uso para crear un horario de rampa a través del API Gateway
"""
from commons.api_client import APIClient
from commons.config import config
from ....domain.ramp_schedule.dto.requests.ramp_schedule_requests import CreateRampScheduleRequest
from ....domain.ramp_schedule.dto.responses.ramp_schedule_responses import RampScheduleCreatedResponse


class CreateRampScheduleUseCase:
    """Caso de uso para crear un horario de rampa"""
    
    def __init__(self):
        self.location_client = APIClient(base_url=config.LOCATION_SERVICE_URL)
    
    async def execute(self, request: CreateRampScheduleRequest, access_token: str = "") -> RampScheduleCreatedResponse:
        """Ejecutar el caso de uso"""
        
        # Preparar datos para el location_service
        payload = {
            "ramp_id": request.ramp_id,
            "day_of_week": request.day_of_week,
            "name": request.name,
            "start_time": request.start_time.strftime("%H:%M:%S"),
            "end_time": request.end_time.strftime("%H:%M:%S"),
            "is_active": request.is_active
        }
        
        # Llamar al location_service
        async with self.location_client as client:
            response = await client.post(
                f"{config.API_PREFIX}/ramp-schedules",
                data=payload,
                headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
            )
        
        # Retornar respuesta
        return RampScheduleCreatedResponse(**response)

