"""
Use case para crear horarios de sucursal desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient, HTTPError
from commons.config import config
from ....domain.schedule.dto.requests.schedule_requests import CreateBranchScheduleRequest
from ....domain.schedule.dto.responses.schedule_responses import CreateBranchScheduleResponse


class CreateBranchScheduleUseCase:
    """Use case para crear horarios de sucursal usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, request: CreateBranchScheduleRequest, access_token: str = "") -> CreateBranchScheduleResponse:
        """
        Crear horario de sucursal desde el reservation_service
        
        Args:
            request: DTO con los datos del horario
            access_token: Token de acceso para autenticación
            
        Returns:
            CreateBranchScheduleResponse: Respuesta con el horario creado
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                # Serializar el request a JSON para manejar tipos como time y date
                import json
                request_json = json.loads(request.json())
                
                response = await client.post(
                    f"{config.API_PREFIX}/schedules/",
                    data=request_json,
                    headers=headers
                )
                
                if response:
                    # El reservation service retorna directamente CreateBranchScheduleResponse
                    # que solo tiene id y message
                    return CreateBranchScheduleResponse(
                        success=True,
                        message=response.get("message", "Horario creado exitosamente"),
                        schedule_id=response.get("id")
                    )
                
                return CreateBranchScheduleResponse(
                    success=False,
                    message="Error creando horario",
                    schedule_id=0
                )
                
        except HTTPError as e:
            # Propagar errores HTTP directamente
            print(f"Error HTTP creando horario: {e}")
            raise e
        except Exception as e:
            print(f"Error inesperado creando horario: {e}")
            return CreateBranchScheduleResponse(
                success=False,
                message=f"Error creando horario: {str(e)}",
                schedule_id=0
            ) 