"""
Caso de uso para actualizar un estado
"""
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.entities.state import State
from ...domain.dto.requests.state_requests import UpdateStateRequest
from ...domain.dto.responses.state_responses import StateUpdatedResponse
from ...domain.exceptions.location_exceptions import StateNotFoundException, StateAlreadyExistsException, CountryNotFoundException


class UpdateStateUseCase:
    """Caso de uso para actualizar un estado"""
    
    def __init__(self, state_repository: StateRepository, country_repository: CountryRepository):
        self.state_repository = state_repository
        self.country_repository = country_repository
    
    async def execute(self, state_id: int, request: UpdateStateRequest) -> StateUpdatedResponse:
        """Ejecutar el caso de uso"""
        # Verificar si el estado existe
        existing_state = await self.state_repository.get_by_id(state_id)
        if not existing_state:
            raise StateNotFoundException(
                f"No se encontró el estado con ID {state_id}",
                entity_id=state_id
            )
        
        # Verificar si el código ya existe (si se está actualizando)
        if request.code and request.code != existing_state.code:
            if await self.state_repository.exists_by_code(request.code, exclude_id=state_id):
                raise StateAlreadyExistsException(
                    f"Ya existe un estado con el código '{request.code}'",
                    code=request.code
                )
        
        # Verificar que el país existe (si se está actualizando)
        country_id = request.country_id if request.country_id is not None else existing_state.country_id
        if request.country_id is not None:
            country = await self.country_repository.get_by_id(request.country_id)
            if not country:
                raise CountryNotFoundException(
                    f"No se encontró el país con ID {request.country_id}",
                    entity_id=request.country_id
                )
        
        # Crear la entidad estado con los datos actualizados
        updated_state = State(
            id=state_id,
            name=request.name if request.name is not None else existing_state.name,
            code=request.code if request.code is not None else existing_state.code,
            country_id=country_id,
            is_active=request.is_active if request.is_active is not None else existing_state.is_active,
            created_at=existing_state.created_at,
            updated_at=existing_state.updated_at
        )
        
        # Actualizar en el repositorio
        await self.state_repository.update(state_id, updated_state)
        
        return StateUpdatedResponse(
            id=state_id,
            message="Estado actualizado exitosamente"
        ) 