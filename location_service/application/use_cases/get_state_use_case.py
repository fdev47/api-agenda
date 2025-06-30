"""
Caso de uso para obtener un estado por ID
"""
from typing import Optional
from ...domain.dto.responses.state_responses import StateResponse
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.exceptions.location_exceptions import StateNotFoundException


class GetStateUseCase:
    """Caso de uso para obtener un estado por ID"""
    
    def __init__(self, state_repository: StateRepository, country_repository: CountryRepository):
        self.state_repository = state_repository
        self.country_repository = country_repository
    
    async def execute(self, state_id: int) -> StateResponse:
        """Ejecutar el caso de uso"""
        
        # Buscar el estado en el repositorio
        state = await self.state_repository.get_by_id(state_id)
        
        if not state:
            raise StateNotFoundException(
                f"No se encontró el estado con ID {state_id}",
                entity_id=state_id
            )
        
        # Obtener información del país
        country = await self.country_repository.get_by_id(state.country_id)
        country_name = country.name if country else "N/A"
        
        # Retornar respuesta
        return StateResponse(
            id=state.id,
            name=state.name,
            code=state.code,
            country_id=state.country_id,
            country_name=country_name,
            is_active=state.is_active,
            created_at=state.created_at,
            updated_at=state.updated_at
        ) 