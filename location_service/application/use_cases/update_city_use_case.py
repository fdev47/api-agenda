"""
Caso de uso para actualizar una ciudad
"""
from ...domain.interfaces.city_repository import CityRepository
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.entities.city import City
from ...domain.dto.requests.city_requests import UpdateCityRequest
from ...domain.dto.responses.city_responses import CityUpdatedResponse
from ...domain.exceptions.location_exceptions import CityNotFoundException, CityAlreadyExistsException, StateNotFoundException


class UpdateCityUseCase:
    """Caso de uso para actualizar una ciudad"""
    
    def __init__(
        self, 
        city_repository: CityRepository,
        state_repository: StateRepository,
        country_repository: CountryRepository
    ):
        self.city_repository = city_repository
        self.state_repository = state_repository
        self.country_repository = country_repository
    
    async def execute(self, city_id: int, request: UpdateCityRequest) -> CityUpdatedResponse:
        """Ejecutar el caso de uso"""
        # Verificar si la ciudad existe
        existing_city = await self.city_repository.get_by_id(city_id)
        if not existing_city:
            raise CityNotFoundException(
                f"No se encontró la ciudad con ID {city_id}",
                entity_id=city_id
            )
        
        # Verificar si el código ya existe (si se está actualizando)
        if request.code and request.code != existing_city.code:
            if await self.city_repository.exists_by_code(request.code, exclude_id=city_id):
                raise CityAlreadyExistsException(
                    f"Ya existe una ciudad con el código '{request.code}'",
                    code=request.code
                )
        
        # Verificar que el estado existe (si se está actualizando)
        state_id = request.state_id if request.state_id is not None else existing_city.state_id
        if request.state_id is not None:
            state = await self.state_repository.get_by_id(request.state_id)
            if not state:
                raise StateNotFoundException(
                    f"No se encontró el estado con ID {request.state_id}",
                    entity_id=request.state_id
                )
        
        # Crear la entidad ciudad con los datos actualizados
        updated_city = City(
            id=city_id,
            name=request.name if request.name is not None else existing_city.name,
            code=request.code if request.code is not None else existing_city.code,
            state_id=state_id,
            is_active=request.is_active if request.is_active is not None else existing_city.is_active,
            created_at=existing_city.created_at,
            updated_at=existing_city.updated_at
        )
        
        # Actualizar en el repositorio
        await self.city_repository.update(city_id, updated_city)
        
        return CityUpdatedResponse(
            id=city_id,
            message="Ciudad actualizada exitosamente"
        ) 