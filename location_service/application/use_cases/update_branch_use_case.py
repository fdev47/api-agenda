"""
Caso de uso para actualizar una sucursal
"""
from ...domain.interfaces.branch_repository import BranchRepository
from ...domain.interfaces.local_repository import LocalRepository
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.city_repository import CityRepository
from ...domain.entities.branch import Branch
from ...domain.dto.requests.branch_requests import UpdateBranchRequest
from ...domain.dto.responses.branch_responses import BranchUpdatedResponse
from ...domain.exceptions.branch_exceptions import BranchNotFoundException, BranchAlreadyExistsException
from ...domain.exceptions.local_exceptions import LocalNotFoundException
from ...domain.exceptions.location_exceptions import CountryNotFoundException, StateNotFoundException, CityNotFoundException


class UpdateBranchUseCase:
    """Caso de uso para actualizar una sucursal"""
    
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
    
    async def execute(self, branch_id: int, request: UpdateBranchRequest) -> BranchUpdatedResponse:
        """Ejecutar el caso de uso"""
        # Verificar si la sucursal existe
        existing_branch = await self.branch_repository.get_by_id(branch_id)
        if not existing_branch:
            raise BranchNotFoundException(
                f"No se encontró la sucursal con ID {branch_id}",
                entity_id=branch_id
            )
        
        # Verificar si el código ya existe (si se está actualizando)
        if request.code and request.code != existing_branch.code:
            if await self.branch_repository.exists_by_code(request.code, exclude_id=branch_id):
                raise BranchAlreadyExistsException(
                    f"Ya existe una sucursal con el código '{request.code}'",
                    code=request.code
                )
        
        # Verificar relaciones si se están actualizando
        local_id = request.local_id if request.local_id is not None else existing_branch.local_id
        country_id = request.country_id if request.country_id is not None else existing_branch.country_id
        state_id = request.state_id if request.state_id is not None else existing_branch.state_id
        city_id = request.city_id if request.city_id is not None else existing_branch.city_id
        
        # Verificar que el local existe
        if request.local_id is not None:
            local = await self.local_repository.get_by_id(request.local_id)
            if not local:
                raise LocalNotFoundException(
                    f"No se encontró el local con ID {request.local_id}",
                    entity_id=request.local_id
                )
        
        # Verificar que el país existe
        if request.country_id is not None:
            country = await self.country_repository.get_by_id(request.country_id)
            if not country:
                raise CountryNotFoundException(
                    f"No se encontró el país con ID {request.country_id}",
                    entity_id=request.country_id
                )
        
        # Verificar que el estado existe
        if request.state_id is not None:
            state = await self.state_repository.get_by_id(request.state_id)
            if not state:
                raise StateNotFoundException(
                    f"No se encontró el estado con ID {request.state_id}",
                    entity_id=request.state_id
                )
        
        # Verificar que la ciudad existe
        if request.city_id is not None:
            city = await self.city_repository.get_by_id(request.city_id)
            if not city:
                raise CityNotFoundException(
                    f"No se encontró la ciudad con ID {request.city_id}",
                    entity_id=request.city_id
                )
        
        # Verificar relaciones jerárquicas si se están actualizando
        if request.state_id is not None and request.country_id is not None:
            state = await self.state_repository.get_by_id(request.state_id)
            if state.country_id != request.country_id:
                raise StateNotFoundException(
                    f"El estado con ID {request.state_id} no pertenece al país con ID {request.country_id}",
                    entity_id=request.state_id
                )
        
        if request.city_id is not None and request.state_id is not None:
            city = await self.city_repository.get_by_id(request.city_id)
            if city.state_id != request.state_id:
                raise CityNotFoundException(
                    f"La ciudad con ID {request.city_id} no pertenece al estado con ID {request.state_id}",
                    entity_id=request.city_id
                )
        
        # Crear la entidad sucursal con los datos actualizados
        updated_branch = Branch(
            id=branch_id,
            name=request.name if request.name is not None else existing_branch.name,
            code=request.code if request.code is not None else existing_branch.code,
            local_id=local_id,
            country_id=country_id,
            state_id=state_id,
            city_id=city_id,
            address=request.address if request.address is not None else existing_branch.address,
            ramps=request.ramps if request.ramps is not None else existing_branch.ramps,
            is_active=request.is_active if request.is_active is not None else existing_branch.is_active,
            created_at=existing_branch.created_at,
            updated_at=existing_branch.updated_at
        )
        
        # Actualizar en el repositorio
        await self.branch_repository.update(branch_id, updated_branch)
        
        return BranchUpdatedResponse(
            id=branch_id,
            message="Sucursal actualizada exitosamente"
        ) 