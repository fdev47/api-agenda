"""
Caso de uso para listar países
"""
from typing import List
from ...domain.dto.requests.country_requests import CountryFilterRequest
from ...domain.dto.responses.country_responses import CountryResponse, CountryListResponse
from ...domain.interfaces.country_repository import CountryRepository


class ListCountriesUseCase:
    """Caso de uso para listar países"""
    
    def __init__(self, country_repository: CountryRepository):
        self.country_repository = country_repository
    
    async def execute(self, filter_request: CountryFilterRequest) -> CountryListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener países del repositorio
        countries, total = await self.country_repository.get_all(filter_request)
        
        # Convertir a DTOs de respuesta
        country_responses = [
            CountryResponse(
                id=country.id,
                name=country.name,
                code=country.code,
                phone_code=country.phone_code,
                is_active=country.is_active,
                created_at=country.created_at,
                updated_at=country.updated_at
            )
            for country in countries
        ]
        
        # Retornar respuesta
        return CountryListResponse(
            countries=country_responses,
            total=total,
            limit=filter_request.limit,
            offset=filter_request.offset
        ) 