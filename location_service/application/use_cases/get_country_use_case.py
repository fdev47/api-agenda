"""
Caso de uso para obtener un país por ID
"""
from typing import Optional
from ...domain.dto.responses.country_responses import CountryResponse
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.exceptions import CountryNotFoundException


class GetCountryByIdUseCase:
    """Caso de uso para obtener un país por ID"""
    
    def __init__(self, country_repository: CountryRepository):
        self.country_repository = country_repository
    
    async def execute(self, country_id: int) -> CountryResponse:
        """Ejecutar el caso de uso"""
        
        # Buscar el país en el repositorio
        country = await self.country_repository.get_by_id(country_id)
        
        if not country:
            raise CountryNotFoundException(country_id=str(country_id))
        
        # Retornar respuesta
        return CountryResponse(
            id=country.id,
            name=country.name,
            code=country.code,
            phone_code=country.phone_code,
            is_active=country.is_active,
            created_at=country.created_at,
            updated_at=country.updated_at
        ) 