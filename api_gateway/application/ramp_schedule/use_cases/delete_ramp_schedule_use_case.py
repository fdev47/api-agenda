"""
Caso de uso para eliminar un horario de rampa
"""
from commons.api_client import APIClient
from commons.config import config
from ....domain.ramp_schedule.dto.responses.ramp_schedule_responses import RampScheduleDeletedResponse


class DeleteRampScheduleUseCase:
    """Caso de uso para eliminar un horario de rampa"""
    
    def __init__(self):
        self.location_client = APIClient(base_url=config.LOCATION_SERVICE_URL)
    
    async def execute(self, schedule_id: int, access_token: str = "") -> RampScheduleDeletedResponse:
        """Ejecutar el caso de uso"""
        
        # Llamar al location_service
        async with self.location_client as client:
            response = await client.delete(
                f"{config.API_PREFIX}/ramp-schedules/{schedule_id}",
                headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
            )
        
        # Retornar respuesta
        return RampScheduleDeletedResponse(**response)

