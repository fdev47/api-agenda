"""
Caso de uso para actualizar un país
"""
from typing import Optional
from ...domain.entities.country import Country
from ...domain.dto.requests.country_requests import UpdateCountryRequest
from ...domain.dto.responses.country_responses import CountryResponse
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.exceptions import CountryNotFoundException, CountryAlreadyExistsException


class UpdateCountryUseCase:
    """Caso de uso para actualizar un país"""
    
    def __init__(self, country_repository: CountryRepository):
        self.country_repository = country_repository
    
    async def execute(self, country_id: int, request: UpdateCountryRequest) -> CountryResponse:
        """Ejecutar el caso de uso"""
        
        # Buscar el país existente
        existing_country = await self.country_repository.get_by_id(country_id)
        if not existing_country:
            raise CountryNotFoundException(country_id=str(country_id))
        
        # Verificar si el código ya existe en otro país
        if request.code and request.code != existing_country.code:
            if await self.country_repository.exists_by_code(request.code, exclude_id=country_id):
                raise CountryAlreadyExistsException(code=request.code)
        
        # Crear entidad actualizada
        updated_country = Country(
            id=country_id,
            name=request.name or existing_country.name,
            code=request.code or existing_country.code,
            phone_code=request.phone_code if request.phone_code is not None else existing_country.phone_code,
            is_active=request.is_active if request.is_active is not None else existing_country.is_active,
            created_at=existing_country.created_at,
            updated_at=existing_country.updated_at
        )
        
        # Guardar en el repositorio
        saved_country = await self.country_repository.update(country_id, updated_country)
        
        if not saved_country:
            raise CountryNotFoundException(country_id=str(country_id))
        
        # Retornar respuesta
        return CountryResponse(
            id=saved_country.id,
            name=saved_country.name,
            code=saved_country.code,
            phone_code=saved_country.phone_code,
            is_active=saved_country.is_active,
            created_at=saved_country.created_at,
            updated_at=saved_country.updated_at
        ) 