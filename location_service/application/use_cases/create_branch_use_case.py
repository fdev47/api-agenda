"""
Caso de uso para crear una sucursal
"""
from ...domain.interfaces.branch_repository import BranchRepository
from ...domain.interfaces.local_repository import LocalRepository
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.city_repository import CityRepository
from ...domain.entities.branch import Branch
from ...domain.dto.requests.branch_requests import CreateBranchRequest
from ...domain.dto.responses.branch_responses import BranchCreatedResponse
from ...domain.exceptions.branch_exceptions import BranchAlreadyExistsException
from ...domain.exceptions.local_exceptions import LocalNotFoundException
from ...domain.exceptions.location_exceptions import CountryNotFoundException, StateNotFoundException, CityNotFoundException


class CreateBranchUseCase:
    """Caso de uso para crear una sucursal"""
    
    def __init__(
        self, 
        branch_repository: BranchRepository,
        local_repository: LocalRepository,
        country_repository: CountryRepository,
        state_repository: StateRepository,
        city_repository: CityRepository
    ):
        self.branch_repository = branch_repository
        self.local_repository = local_repository
        self.country_repository = country_repository
        self.state_repository = state_repository
        self.city_repository = city_repository
    
    async def execute(self, request: CreateBranchRequest) -> BranchCreatedResponse:
        """Ejecutar el caso de uso"""
        # Verificar si ya existe una sucursal con el mismo código
        if await self.branch_repository.exists_by_code(request.code):
            raise BranchAlreadyExistsException(
                f"Ya existe una sucursal con el código '{request.code}'",
                code=request.code
            )
        
        # Verificar que el local existe
        local = await self.local_repository.get_by_id(request.local_id)
        if not local:
            raise LocalNotFoundException(
                f"No se encontró el local con ID {request.local_id}",
                entity_id=request.local_id
            )
        
        # Verificar que el país existe
        country = await self.country_repository.get_by_id(request.country_id)
        if not country:
            raise CountryNotFoundException(
                f"No se encontró el país con ID {request.country_id}",
                entity_id=request.country_id
            )
        
        # Verificar que el estado existe
        state = await self.state_repository.get_by_id(request.state_id)
        if not state:
            raise StateNotFoundException(
                f"No se encontró el estado con ID {request.state_id}",
                entity_id=request.state_id
            )
        
        # Verificar que la ciudad existe
        city = await self.city_repository.get_by_id(request.city_id)
        if not city:
            raise CityNotFoundException(
                f"No se encontró la ciudad con ID {request.city_id}",
                entity_id=request.city_id
            )
        
        # Verificar que el estado pertenece al país
        if state.country_id != request.country_id:
            raise StateNotFoundException(
                f"El estado con ID {request.state_id} no pertenece al país con ID {request.country_id}",
                entity_id=request.state_id
            )
        
        # Verificar que la ciudad pertenece al estado
        if city.state_id != request.state_id:
            raise CityNotFoundException(
                f"La ciudad con ID {request.city_id} no pertenece al estado con ID {request.state_id}",
                entity_id=request.city_id
            )
        
        # Crear la entidad sucursal
        branch = Branch(
            name=request.name,
            code=request.code,
            local_id=request.local_id,
            country_id=request.country_id,
            state_id=request.state_id,
            city_id=request.city_id,
            address=request.address,
            ramps=request.ramps,
            is_active=request.is_active
        )
        
        # Guardar en el repositorio
        created_branch = await self.branch_repository.create(branch)
        
        return BranchCreatedResponse(
            id=created_branch.id,
            message="Sucursal creada exitosamente"
        ) 