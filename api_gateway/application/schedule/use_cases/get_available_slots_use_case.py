"""
Use case para obtener slots disponibles desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from ....domain.schedule.dto.requests.schedule_requests import GetAvailableSlotsRequest
from ....domain.schedule.dto.responses.schedule_responses import AvailableSlotsResponse, AvailableSlotResponse


class GetAvailableSlotsUseCase:
    """Use case para obtener slots disponibles usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, request: GetAvailableSlotsRequest, access_token: str = "") -> AvailableSlotsResponse:
        """
        Obtener slots disponibles desde el reservation_service
        
        Args:
            request: DTO con los datos de la consulta
            access_token: Token de acceso para autenticación
            
        Returns:
            AvailableSlotsResponse: Respuesta con los slots disponibles
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            params = {
                "branch_id": request.branch_id,
                "schedule_date": request.schedule_date.isoformat()
            }
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/schedules/available-slots",
                    params=params,
                    headers=headers
                )
                
                if response:
                    slots = [AvailableSlotResponse(**slot) for slot in response.get("slots", [])]
                    return AvailableSlotsResponse(
                        branch_id=response.get("branch_id", request.branch_id),
                        schedule_date=request.schedule_date,
                        slots=slots,
                        total_slots=response.get("total_slots", len(slots)),
                        available_slots=response.get("available_slots", len([s for s in slots if s.is_available]))
                    )
                
                return AvailableSlotsResponse(
                    branch_id=request.branch_id,
                    schedule_date=request.schedule_date,
                    slots=[],
                    total_slots=0,
                    available_slots=0
                )
                
        except Exception as e:
            print(f"Error obteniendo slots disponibles: {e}")
            return AvailableSlotsResponse(
                branch_id=request.branch_id,
                schedule_date=request.schedule_date,
                slots=[],
                total_slots=0,
                available_slots=0
            ) 