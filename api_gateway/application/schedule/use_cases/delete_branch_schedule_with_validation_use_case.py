"""
Use case para eliminar horarios de sucursal con validación desde el API Gateway
"""
from typing import Optional
from commons.api_client import APIClient, HTTPError
from commons.config import config
from ....domain.schedule.dto.responses.schedule_responses import DeleteBranchScheduleResponse
from ....domain.schedule.dto.responses.schedule_validation_responses import ValidateScheduleDeletionResponse


class DeleteBranchScheduleWithValidationUseCase:
    """Use case para eliminar horarios de sucursal con validación usando reservation_service"""
    
    def __init__(self):
        self.reservation_service_url = config.RESERVATION_SERVICE_URL
    
    async def execute(self, schedule_id: int, access_token: str = "") -> DeleteBranchScheduleResponse:
        """
        Eliminar horario de sucursal desde el reservation_service
        
        Args:
            schedule_id: ID del horario a eliminar
            access_token: Token de acceso para autenticación
            
        Returns:
            DeleteBranchScheduleResponse: Respuesta con el horario eliminado
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.delete(
                    f"{config.API_PREFIX}/schedules/{schedule_id}",
                    headers=headers
                )
                
                if response:
                    return DeleteBranchScheduleResponse(
                        success=response.get("success", True),
                        message=response.get("message", "Horario eliminado exitosamente"),
                        schedule_id=schedule_id
                    )
                
                return DeleteBranchScheduleResponse(
                    success=False,
                    message="Error eliminando horario",
                    schedule_id=schedule_id
                )
                
        except HTTPError as e:
            # Propagar errores HTTP directamente
            print(f"Error HTTP eliminando horario: {e}")
            raise e
        except Exception as e:
            print(f"Error inesperado eliminando horario: {e}")
            return DeleteBranchScheduleResponse(
                success=False,
                message=f"Error eliminando horario: {str(e)}",
                schedule_id=schedule_id
            )
    
    async def validate_deletion(self, schedule_id: int, access_token: str = "") -> ValidateScheduleDeletionResponse:
        """
        Validar eliminación de horario desde el reservation_service
        
        Args:
            schedule_id: ID del horario a validar
            access_token: Token de acceso para autenticación
            
        Returns:
            ValidateScheduleDeletionResponse: Respuesta de validación
        """
        try:
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
            async with APIClient(self.reservation_service_url, "") as client:
                response = await client.get(
                    f"{config.API_PREFIX}/schedules/{schedule_id}/validate-deletion",
                    headers=headers
                )
                
                if response:
                    impact_analysis = None
                    if response.get("impact_analysis"):
                        impact_analysis = response["impact_analysis"]
                    
                    return ValidateScheduleDeletionResponse(
                        can_delete=response.get("can_delete", True),
                        requires_rescheduling=response.get("requires_rescheduling", False),
                        message=response.get("message", "Validación completada"),
                        impact_analysis=impact_analysis
                    )
                
                return ValidateScheduleDeletionResponse(
                    can_delete=False,
                    requires_rescheduling=False,
                    message="Error en validación",
                    impact_analysis=None
                )
                
        except HTTPError as e:
            # Propagar errores HTTP directamente
            print(f"Error HTTP validando eliminación: {e}")
            raise e
        except Exception as e:
            print(f"Error inesperado validando eliminación: {e}")
            return ValidateScheduleDeletionResponse(
                can_delete=False,
                requires_rescheduling=False,
                message=f"Error en validación: {str(e)}",
                impact_analysis=None
            ) 