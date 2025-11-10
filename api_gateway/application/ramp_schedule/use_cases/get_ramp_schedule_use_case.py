"""
Caso de uso para obtener un horario de rampa por ID
"""
from commons.api_client import APIClient
from commons.config import config
from ....domain.ramp_schedule.dto.responses.ramp_schedule_responses import RampScheduleResponse


class GetRampScheduleUseCase:
    """Caso de uso para obtener un horario de rampa por ID"""
    
    def __init__(self):
        self.location_client = APIClient(base_url=config.LOCATION_SERVICE_URL)
    
    async def execute(self, schedule_id: int, access_token: str = "") -> RampScheduleResponse:
        """Ejecutar el caso de uso"""
        
        # Llamar al location_service
        async with self.location_client as client:
            response = await client.get(
                f"{config.API_PREFIX}/ramp-schedules/{schedule_id}",
                headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
            )
        
        # Retornar respuesta
        return RampScheduleResponse(**response)

