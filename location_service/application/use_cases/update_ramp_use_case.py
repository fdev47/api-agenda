"""
Caso de uso para actualizar una rampa
"""
from datetime import datetime
from ...domain.entities.ramp import Ramp
from ...domain.interfaces.ramp_repository import RampRepository
from ...domain.dto.requests.update_ramp_request import UpdateRampRequest
from ...domain.dto.responses.ramp_response import RampResponse
from ...domain.exceptions import RampNotFoundException, RampValidationException


class UpdateRampUseCase:
    """Caso de uso para actualizar una rampa"""
    
    def __init__(self, ramp_repository: RampRepository):
        self.ramp_repository = ramp_repository
    
    async def execute(self, ramp_id: int, request: UpdateRampRequest) -> RampResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener la rampa existente
        existing_ramp = await self.ramp_repository.get_by_id(ramp_id)
        
        if not existing_ramp:
            raise RampNotFoundException(
                f"Rampa con ID {ramp_id} no encontrada",
                entity_id=ramp_id
            )
        
        # Validar campos
        field_errors = {}
        
        if request.name is not None and not request.name.strip():
            field_errors["name"] = "El nombre de la rampa no puede estar vacío"
        
        if field_errors:
            raise RampValidationException(
                "Error de validación en la actualización de la rampa",
                field_errors=field_errors
            )
        
        # Actualizar campos
        if request.name is not None:
            existing_ramp.update_name(request.name)
        
        if request.is_available is not None:
            if request.is_available:
                existing_ramp.make_available()
            else:
                existing_ramp.make_unavailable()
        
        # Guardar en el repositorio
        updated_ramp = await self.ramp_repository.update(existing_ramp)
        
        # Retornar respuesta
        return RampResponse(
            id=updated_ramp.id,
            name=updated_ramp.name,
            is_available=updated_ramp.is_available,
            branch_id=updated_ramp.branch_id,
            created_at=updated_ramp.created_at,
            updated_at=updated_ramp.updated_at
        ) 