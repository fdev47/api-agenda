"""
Caso de uso para listar ciudades
"""
from typing import List
from ...domain.dto.requests.city_requests import CityFilterRequest
from ...domain.dto.responses.city_responses import CityResponse, CityListResponse
from ...domain.interfaces.city_repository import CityRepository
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.country_repository import CountryRepository


class ListCitiesUseCase:
    """Caso de uso para listar ciudades"""
    
    def __init__(
        self, 
        city_repository: CityRepository,
        state_repository: StateRepository,
        country_repository: CountryRepository
    ):
        self.city_repository = city_repository
        self.state_repository = state_repository
        self.country_repository = country_repository
    
    async def execute(self, filter_request: CityFilterRequest) -> CityListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener ciudades del repositorio
        cities, total = await self.city_repository.get_all(filter_request)
        
        # Convertir a DTOs de respuesta con información relacionada
        city_responses = []
        for city in cities:
            # Obtener información del estado
            state = await self.state_repository.get_by_id(city.state_id)
            state_name = state.name if state else "N/A"
            
            # Obtener información del país
            country_id = 0
            country_name = "N/A"
            if state:
                country = await self.country_repository.get_by_id(state.country_id)
                country_id = country.id if country else 0
                country_name = country.name if country else "N/A"
            
            city_response = CityResponse(
                id=city.id,
                name=city.name,
                state_id=city.state_id,
                state_name=state_name,
                country_id=country_id,
                country_name=country_name,
                is_active=city.is_active,
                created_at=city.created_at,
                updated_at=city.updated_at
            )
            city_responses.append(city_response)
        
        # Retornar respuesta
        return CityListResponse(
            cities=city_responses,
            total=total,
            limit=filter_request.limit,
            offset=filter_request.offset
        ) 