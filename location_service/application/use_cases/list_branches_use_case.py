"""
Caso de uso para listar sucursales
"""
from ...domain.interfaces.branch_repository import BranchRepository
from ...domain.interfaces.local_repository import LocalRepository
from ...domain.interfaces.country_repository import CountryRepository
from ...domain.interfaces.state_repository import StateRepository
from ...domain.interfaces.city_repository import CityRepository
from ...domain.interfaces.ramp_repository import RampRepository
from ...domain.interfaces.sector_repository import SectorRepository
from ...domain.dto.requests.branch_requests import BranchFilterRequest
from ...domain.dto.responses.branch_responses import BranchListResponse, BranchResponse, RampSummaryResponse, SectorSummaryResponse


class ListBranchesUseCase:
    """Caso de uso para listar sucursales"""
    
    def __init__(
        self, 
        branch_repository: BranchRepository,
        local_repository: LocalRepository,
        country_repository: CountryRepository,
        state_repository: StateRepository,
        city_repository: CityRepository,
        ramp_repository: RampRepository,
        sector_repository: SectorRepository
    ):
        self.branch_repository = branch_repository
        self.local_repository = local_repository
        self.country_repository = country_repository
        self.state_repository = state_repository
        self.city_repository = city_repository
        self.ramp_repository = ramp_repository
        self.sector_repository = sector_repository
    
    async def execute(self, filter_request: BranchFilterRequest) -> BranchListResponse:
        """Ejecutar el caso de uso"""
        # Obtener sucursales del repositorio
        branches, total = await self.branch_repository.list_all(filter_request)
        

        if not branches:
            return BranchListResponse(
                branches=[],
                total=total,
                limit=filter_request.limit,
                offset=filter_request.offset
            )
        

        # Obtener información relacionada para cada sucursal
        branch_responses = []
        for branch in branches:
            local = await self.local_repository.get_by_id(branch.local_id)
            country = await self.country_repository.get_by_id(branch.country_id)
            state = await self.state_repository.get_by_id(branch.state_id)
            city = await self.city_repository.get_by_id(branch.city_id)
            
            # Obtener información real de las rampas
            ramp_responses = []
            for ramp_id in branch.ramps:
                ramp = await self.ramp_repository.get_by_id(ramp_id)
                if ramp:
                    ramp_responses.append(RampSummaryResponse(
                        id=ramp.id,
                        name=ramp.name,
                        is_available=ramp.is_available
                    ))
            
            # Obtener información real de los sectores
            sector_responses = []
            for sector_id in branch.sectors:
                sector = await self.sector_repository.get_by_id(sector_id)
                if sector:
                    sector_responses.append(SectorSummaryResponse(
                        id=sector.id,
                        name=sector.name,
                        sector_type_id=sector.sector_type_id,
                        is_active=sector.is_active
                    ))
            
            branch_response = BranchResponse(
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
                ramps=ramp_responses,
                sectors=sector_responses,
                is_active=branch.is_active,
                created_at=branch.created_at,
                updated_at=branch.updated_at
            )
            branch_responses.append(branch_response)
        
        return BranchListResponse(
            branches=branch_responses,
            total=total,
            limit=filter_request.limit,
            offset=filter_request.offset
        ) 