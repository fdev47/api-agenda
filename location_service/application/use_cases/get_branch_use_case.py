"""
Caso de uso para obtener una sucursal por ID
"""
from ...domain.interfaces.branch_repository import BranchRepository
from ...domain.interfaces.local_repository import LocalRepository
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.city_repository import CityRepository
from ...domain.dto.responses.branch_responses import BranchResponse
from ...domain.exceptions.branch_exceptions import BranchNotFoundException


class GetBranchUseCase:
    """Caso de uso para obtener una sucursal por ID"""
    
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
    
    async def execute(self, branch_id: int) -> BranchResponse:
        """Ejecutar el caso de uso"""
        # Obtener la sucursal del repositorio
        branch = await self.branch_repository.get_by_id(branch_id)
        
        if not branch:
            raise BranchNotFoundException(
                f"No se encontró la sucursal con ID {branch_id}",
                entity_id=branch_id
            )
        
        # Obtener información relacionada
        local = await self.local_repository.get_by_id(branch.local_id)
        country = await self.country_repository.get_by_id(branch.country_id)
        state = await self.state_repository.get_by_id(branch.state_id)
        city = await self.city_repository.get_by_id(branch.city_id)
        
        return BranchResponse(
            id=branch.id,
            name=branch.name,
            code=branch.code,
            local_id=branch.local_id,
            local_name=local.name if local else "N/A",
            local_phone=local.phone if local else None,
            local_email=local.email if local else None,
            country_id=branch.country_id,
            country_name=country.name if country else "N/A",
            state_id=branch.state_id,
            state_name=state.name if state else "N/A",
            city_id=branch.city_id,
            city_name=city.name if city else "N/A",
            address=branch.address,
            ramps=branch.ramps,
            is_active=branch.is_active,
            created_at=branch.created_at,
            updated_at=branch.updated_at
        ) 