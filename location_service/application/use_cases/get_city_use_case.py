"""
Caso de uso para obtener una ciudad por ID
"""
from ...domain.interfaces.city_repository import CityRepository
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.dto.responses.city_responses import CityResponse
from ...domain.exceptions.location_exceptions import CityNotFoundException


class GetCityUseCase:
    """Caso de uso para obtener una ciudad por ID"""
    
    def __init__(
        self, 
        city_repository: CityRepository,
        state_repository: StateRepository,
        country_repository: CountryRepository
    ):
        self.city_repository = city_repository
        self.state_repository = state_repository
        self.country_repository = country_repository
    
    async def execute(self, city_id: int) -> CityResponse:
        """Ejecutar el caso de uso"""
        # Obtener la ciudad del repositorio
        city = await self.city_repository.get_by_id(city_id)
        
        if not city:
            raise CityNotFoundException(
                f"No se encontró la ciudad con ID {city_id}",
                entity_id=city_id
            )
        
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
        
        return CityResponse(
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