"""
Use case para actualizar horarios de sucursal desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient, HTTPError
from commons.config import config
from ....domain.schedule.dto.requests.schedule_requests import UpdateBranchScheduleRequest
from ....domain.schedule.dto.responses.schedule_responses import UpdateBranchScheduleResponse, BranchScheduleResponse


class UpdateBranchScheduleUseCase:
    """Use case para actualizar horarios de sucursal usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, schedule_id: int, request: UpdateBranchScheduleRequest, access_token: str = "", auto_reschedule: bool = False) -> UpdateBranchScheduleResponse:
        """
        Actualizar horario de sucursal desde el reservation_service
        
        Args:
            schedule_id: ID del horario a actualizar
            request: DTO con los datos de actualización
            access_token: Token de acceso para autenticación
            auto_reschedule: Aplicar cambios automáticamente
            
        Returns:
            UpdateBranchScheduleResponse: Respuesta con el horario actualizado
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            params = {"auto_reschedule": auto_reschedule}
            
            async with APIClient(self.reservation_service_url, "") as client:
                # Serializar el request a JSON para manejar tipos como time y date
                import json
                request_json = json.loads(request.json(exclude_none=True))
                
                response = await client.put(
                    f"{config.API_PREFIX}/schedules/{schedule_id}/update-with-validation",
                    data=request_json,
                    params=params,
                    headers=headers
                )
                
                if response:
                    schedule = None
                    if response.get("schedule"):
                        schedule = BranchScheduleResponse(**response["schedule"])
                    
                    return UpdateBranchScheduleResponse(
                        success=response.get("success", True),
                        message=response.get("message", "Horario actualizado exitosamente"),
                        requires_confirmation=response.get("requires_confirmation", False),
                        schedule=schedule,
                        impact_analysis=response.get("impact_analysis")
                    )
                
                return UpdateBranchScheduleResponse(
                    success=False,
                    message="Error actualizando horario",
                    requires_confirmation=False,
                    schedule=None,
                    impact_analysis=None
                )
                
        except HTTPError as e:
            # Propagar errores HTTP directamente
            print(f"Error HTTP actualizando horario: {e}")
            raise e
        except Exception as e:
            print(f"Error inesperado actualizando horario: {e}")
            return UpdateBranchScheduleResponse(
                success=False,
                message=f"Error actualizando horario: {str(e)}",
                requires_confirmation=False,
                schedule=None,
                impact_analysis=None
            ) 