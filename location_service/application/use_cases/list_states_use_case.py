"""
Caso de uso para listar estados
"""
from typing import List
from ...domain.dto.requests.state_requests import StateFilterRequest
from ...domain.dto.responses.state_responses import StateResponse, StateListResponse
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.country_repository import CountryRepository


class ListStatesUseCase:
    """Caso de uso para listar estados"""
    
    def __init__(self, state_repository: StateRepository, country_repository: CountryRepository):
        self.state_repository = state_repository
        self.country_repository = country_repository
    
    async def execute(self, filter_request: StateFilterRequest) -> StateListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener estados del repositorio
        states, total = await self.state_repository.get_all(filter_request)
        
        # Convertir a DTOs de respuesta con información relacionada
        state_responses = []
        for state in states:
            # Obtener información del país
            country = await self.country_repository.get_by_id(state.country_id)
            country_name = country.name if country else "N/A"
            
            state_response = StateResponse(
                id=state.id,
                name=state.name,
                code=state.code,
                country_id=state.country_id,
                country_name=country_name,
                is_active=state.is_active,
                created_at=state.created_at,
                updated_at=state.updated_at
            )
            state_responses.append(state_response)
        
        # Retornar respuesta
        return StateListResponse(
            states=state_responses,
            total=total,
            limit=filter_request.limit,
            offset=filter_request.offset
        ) 