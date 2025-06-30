"""
Caso de uso para crear un país
"""
from typing import Optional
from ...domain.entities.country import Country
from ...domain.dto.requests.country_requests import CreateCountryRequest
from ...domain.dto.responses.country_responses import CountryResponse
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.exceptions import CountryAlreadyExistsException


class CreateCountryUseCase:
    """Caso de uso para crear un país"""
    
    def __init__(self, country_repository: CountryRepository):
        self.country_repository = country_repository
    
    async def execute(self, request: CreateCountryRequest) -> CountryResponse:
        """Ejecutar el caso de uso"""
        
        # Verificar si ya existe un país con el mismo código
        if await self.country_repository.exists_by_code(request.code):
            raise CountryAlreadyExistsException(code=request.code)
        
        # Crear la entidad Country
        country = Country(
            name=request.name,
            code=request.code,
            phone_code=request.phone_code,
            is_active=True
        )
        
        # Guardar en el repositorio
        created_country = await self.country_repository.create(country)
        
        # Retornar respuesta
        return CountryResponse(
            id=created_country.id,
            name=created_country.name,
            code=created_country.code,
            phone_code=created_country.phone_code,
            is_active=created_country.is_active,
            created_at=created_country.created_at,
            updated_at=created_country.updated_at
        ) 