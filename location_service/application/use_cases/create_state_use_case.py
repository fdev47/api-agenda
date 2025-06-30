"""
Caso de uso para crear un estado
"""
from typing import Optional
from ...domain.entities.state import State
from ...domain.dto.requests.state_requests import CreateStateRequest
from ...domain.dto.responses.state_responses import StateResponse
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.exceptions import StateAlreadyExistsException, CountryNotFoundException


class CreateStateUseCase:
    """Caso de uso para crear un estado"""
    
    def __init__(self, state_repository: StateRepository, country_repository: CountryRepository):
        self.state_repository = state_repository
        self.country_repository = country_repository
    
    async def execute(self, request: CreateStateRequest) -> StateResponse:
        """Ejecutar el caso de uso"""
        
        # Verificar que el país existe
        country = await self.country_repository.get_by_id(request.country_id)
        if not country:
            raise CountryNotFoundException(country_id=str(request.country_id))
        
        # Verificar si ya existe un estado con el mismo código en el país
        if await self.state_repository.exists_by_code(request.code, exclude_id=None):
            raise StateAlreadyExistsException(code=request.code)
        
        # Crear la entidad State
        state = State(
            name=request.name,
            code=request.code,
            country_id=request.country_id,
            is_active=True
        )
        
        # Guardar en el repositorio
        created_state = await self.state_repository.create(state)
        
        # Retornar respuesta
        return StateResponse(
            id=created_state.id,
            name=created_state.name,
            code=created_state.code,
            country_id=created_state.country_id,
            country_name=country.name,
            is_active=created_state.is_active,
            created_at=created_state.created_at,
            updated_at=created_state.updated_at
        ) 