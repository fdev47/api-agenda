"""
Caso de uso para crear una ciudad
"""
from ...domain.interfaces.city_repository import CityRepository
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.entities.city import City
from ...domain.dto.requests.city_requests import CreateCityRequest
from ...domain.dto.responses.city_responses import CityCreatedResponse
from ...domain.exceptions.location_exceptions import CityAlreadyExistsException, StateNotFoundException


class CreateCityUseCase:
    """Caso de uso para crear una ciudad"""
    
    def __init__(
        self, 
        city_repository: CityRepository,
        state_repository: StateRepository,
        country_repository: CountryRepository
    ):
        self.city_repository = city_repository
        self.state_repository = state_repository
        self.country_repository = country_repository
    
    async def execute(self, request: CreateCityRequest) -> CityCreatedResponse:
        """Ejecutar el caso de uso"""
        # Verificar si ya existe una ciudad con el mismo código
        if await self.city_repository.exists_by_code(request.code):
            raise CityAlreadyExistsException(
                f"Ya existe una ciudad con el código '{request.code}'",
                code=request.code
            )
        
        # Verificar que el estado existe
        state = await self.state_repository.get_by_id(request.state_id)
        if not state:
            raise StateNotFoundException(
                f"No se encontró el estado con ID {request.state_id}",
                entity_id=request.state_id
            )
        
        # Crear la entidad ciudad
        city = City(
            name=request.name,
            code=request.code,
            state_id=request.state_id,
            is_active=request.is_active
        )
        
        # Guardar en el repositorio
        created_city = await self.city_repository.create(city)
        
        return CityCreatedResponse(
            id=created_city.id,
            message="Ciudad creada exitosamente"
        ) 