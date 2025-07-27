"""
Container de dependencias para el servicio de ubicaciones
"""
from dependency_injector import containers, providers
from commons.database import db_manager

# Repositorios
from .repositories.country_repository_impl import CountryRepositoryImpl
from .repositories.state_repository_impl import StateRepositoryImpl
from .repositories.city_repository_impl import CityRepositoryImpl
from .repositories.local_repository_impl import LocalRepositoryImpl
from .repositories.branch_repository_impl import BranchRepositoryImpl
from .repositories.ramp_repository_impl import RampRepositoryImpl
from .repositories.sector_repository_impl import SectorRepositoryImpl
from .repositories.sector_type_repository_impl import SectorTypeRepositoryImpl

# Casos de uso
from ..application.use_cases.create_country_use_case import CreateCountryUseCase
from ..application.use_cases.get_country_use_case import GetCountryByIdUseCase
from ..application.use_cases.list_countries_use_case import ListCountriesUseCase
from ..application.use_cases.update_country_use_case import UpdateCountryUseCase
from ..application.use_cases.delete_country_use_case import DeleteCountryUseCase

from ..application.use_cases.create_state_use_case import CreateStateUseCase
from ..application.use_cases.get_state_use_case import GetStateUseCase
from ..application.use_cases.list_states_use_case import ListStatesUseCase
from ..application.use_cases.update_state_use_case import UpdateStateUseCase
from ..application.use_cases.delete_state_use_case import DeleteStateUseCase

from ..application.use_cases.create_city_use_case import CreateCityUseCase
from ..application.use_cases.get_city_use_case import GetCityUseCase
from ..application.use_cases.list_cities_use_case import ListCitiesUseCase
from ..application.use_cases.update_city_use_case import UpdateCityUseCase
from ..application.use_cases.delete_city_use_case import DeleteCityUseCase

from ..application.use_cases.create_local_use_case import CreateLocalUseCase
from ..application.use_cases.get_local_use_case import GetLocalUseCase
from ..application.use_cases.list_locals_use_case import ListLocalsUseCase
from ..application.use_cases.update_local_use_case import UpdateLocalUseCase
from ..application.use_cases.delete_local_use_case import DeleteLocalUseCase

from ..application.use_cases.create_branch_use_case import CreateBranchUseCase
from ..application.use_cases.get_branch_use_case import GetBranchUseCase
from ..application.use_cases.list_branches_use_case import ListBranchesUseCase
from ..application.use_cases.update_branch_use_case import UpdateBranchUseCase
from ..application.use_cases.delete_branch_use_case import DeleteBranchUseCase

from ..application.use_cases.create_ramp_use_case import CreateRampUseCase
from ..application.use_cases.get_ramp_use_case import GetRampUseCase
from ..application.use_cases.list_ramps_use_case import ListRampsUseCase
from ..application.use_cases.update_ramp_use_case import UpdateRampUseCase
from ..application.use_cases.delete_ramp_use_case import DeleteRampUseCase

from ..application.use_cases.create_sector_use_case import CreateSectorUseCase
from ..application.use_cases.get_sector_use_case import GetSectorUseCase
from ..application.use_cases.list_sectors_use_case import ListSectorsUseCase
from ..application.use_cases.update_sector_use_case import UpdateSectorUseCase
from ..application.use_cases.delete_sector_use_case import DeleteSectorUseCase

from ..application.use_cases.create_sector_type_use_case import CreateSectorTypeUseCase
from ..application.use_cases.get_sector_type_use_case import GetSectorTypeUseCase
from ..application.use_cases.list_sector_types_use_case import ListSectorTypesUseCase
from ..application.use_cases.update_sector_type_use_case import UpdateSectorTypeUseCase
from ..application.use_cases.delete_sector_type_use_case import DeleteSectorTypeUseCase


class Container(containers.DeclarativeContainer):
    """Container de dependencias"""
    
    # Configuración
    config = providers.Configuration()
    
    # Base de datos
    db_session = providers.Factory(
        lambda: db_manager.AsyncSessionLocal()
    )
    
    # Repositorios
    country_repository = providers.Factory(
        CountryRepositoryImpl,
        session=db_session
    )
    
    state_repository = providers.Factory(
        StateRepositoryImpl,
        session=db_session
    )
    
    city_repository = providers.Factory(
        CityRepositoryImpl,
        session=db_session
    )
    
    local_repository = providers.Factory(
        LocalRepositoryImpl,
        session=db_session
    )
    
    branch_repository = providers.Factory(
        BranchRepositoryImpl,
        session=db_session
    )
    
    ramp_repository = providers.Factory(
        RampRepositoryImpl,
        session=db_session
    )
    
    sector_repository = providers.Factory(
        SectorRepositoryImpl,
        session=db_session
    )
    
    sector_type_repository = providers.Factory(
        SectorTypeRepositoryImpl,
        session=db_session
    )
    
    # Casos de uso para países
    create_country_use_case = providers.Factory(
        CreateCountryUseCase,
        country_repository=country_repository
    )
    
    get_country_use_case = providers.Factory(
        GetCountryByIdUseCase,
        country_repository=country_repository
    )
    
    list_countries_use_case = providers.Factory(
        ListCountriesUseCase,
        country_repository=country_repository
    )
    
    update_country_use_case = providers.Factory(
        UpdateCountryUseCase,
        country_repository=country_repository
    )
    
    delete_country_use_case = providers.Factory(
        DeleteCountryUseCase,
        country_repository=country_repository
    )
    
    # Casos de uso para estados
    create_state_use_case = providers.Factory(
        CreateStateUseCase,
        state_repository=state_repository,
        country_repository=country_repository
    )
    
    get_state_use_case = providers.Factory(
        GetStateUseCase,
        state_repository=state_repository,
        country_repository=country_repository
    )
    
    list_states_use_case = providers.Factory(
        ListStatesUseCase,
        state_repository=state_repository,
        country_repository=country_repository
    )
    
    update_state_use_case = providers.Factory(
        UpdateStateUseCase,
        state_repository=state_repository,
        country_repository=country_repository
    )
    
    delete_state_use_case = providers.Factory(
        DeleteStateUseCase,
        state_repository=state_repository
    )
    
    # Casos de uso para ciudades
    create_city_use_case = providers.Factory(
        CreateCityUseCase,
        city_repository=city_repository,
        state_repository=state_repository
    )
    
    get_city_use_case = providers.Factory(
        GetCityUseCase,
        city_repository=city_repository,
        state_repository=state_repository,
        country_repository=country_repository
    )
    
    list_cities_use_case = providers.Factory(
        ListCitiesUseCase,
        city_repository=city_repository,
        state_repository=state_repository,
        country_repository=country_repository
    )
    
    update_city_use_case = providers.Factory(
        UpdateCityUseCase,
        city_repository=city_repository,
        state_repository=state_repository
    )
    
    delete_city_use_case = providers.Factory(
        DeleteCityUseCase,
        city_repository=city_repository
    )
    
    # Casos de uso para locales
    create_local_use_case = providers.Factory(
        CreateLocalUseCase,
        local_repository=local_repository
    )
    
    get_local_use_case = providers.Factory(
        GetLocalUseCase,
        local_repository=local_repository
    )
    
    list_locals_use_case = providers.Factory(
        ListLocalsUseCase,
        local_repository=local_repository
    )
    
    update_local_use_case = providers.Factory(
        UpdateLocalUseCase,
        local_repository=local_repository
    )
    
    delete_local_use_case = providers.Factory(
        DeleteLocalUseCase,
        local_repository=local_repository
    )
    
    # Casos de uso para sucursales
    create_branch_use_case = providers.Factory(
        CreateBranchUseCase,
        branch_repository=branch_repository,
        local_repository=local_repository,
        country_repository=country_repository,
        state_repository=state_repository,
        city_repository=city_repository
    )
    
    get_branch_use_case = providers.Factory(
        GetBranchUseCase,
        branch_repository=branch_repository,
        local_repository=local_repository,
        country_repository=country_repository,
        state_repository=state_repository,
        city_repository=city_repository
    )
    
    list_branches_use_case = providers.Factory(
        ListBranchesUseCase,
        branch_repository=branch_repository,
        local_repository=local_repository,
        country_repository=country_repository,
        state_repository=state_repository,
        city_repository=city_repository
    )
    
    update_branch_use_case = providers.Factory(
        UpdateBranchUseCase,
        branch_repository=branch_repository,
        local_repository=local_repository,
        country_repository=country_repository,
        state_repository=state_repository,
        city_repository=city_repository
    )
    
    delete_branch_use_case = providers.Factory(
        DeleteBranchUseCase,
        branch_repository=branch_repository
    )

    # Casos de uso para rampas
    create_ramp_use_case = providers.Factory(
        CreateRampUseCase,
        ramp_repository=ramp_repository
    )
    
    get_ramp_use_case = providers.Factory(
        GetRampUseCase,
        ramp_repository=ramp_repository
    )
    
    list_ramps_use_case = providers.Factory(
        ListRampsUseCase,
        ramp_repository=ramp_repository
    )
    
    update_ramp_use_case = providers.Factory(
        UpdateRampUseCase,
        ramp_repository=ramp_repository
    )
    
    delete_ramp_use_case = providers.Factory(
        DeleteRampUseCase,
        ramp_repository=ramp_repository
    )

    # Casos de uso para sectores
    create_sector_use_case = providers.Factory(
        CreateSectorUseCase,
        sector_repository=sector_repository,
        sector_type_repository=sector_type_repository
    )
    
    get_sector_use_case = providers.Factory(
        GetSectorUseCase,
        sector_repository=sector_repository
    )
    
    list_sectors_use_case = providers.Factory(
        ListSectorsUseCase,
        sector_repository=sector_repository
    )
    
    update_sector_use_case = providers.Factory(
        UpdateSectorUseCase,
        sector_repository=sector_repository
    )
    
    delete_sector_use_case = providers.Factory(
        DeleteSectorUseCase,
        sector_repository=sector_repository
    )

    # Casos de uso para tipos de sector
    create_sector_type_use_case = providers.Factory(
        CreateSectorTypeUseCase,
        sector_type_repository=sector_type_repository
    )
    
    get_sector_type_use_case = providers.Factory(
        GetSectorTypeUseCase,
        sector_type_repository=sector_type_repository
    )
    
    list_sector_types_use_case = providers.Factory(
        ListSectorTypesUseCase,
        sector_type_repository=sector_type_repository
    )
    
    update_sector_type_use_case = providers.Factory(
        UpdateSectorTypeUseCase,
        sector_type_repository=sector_type_repository
    )
    
    delete_sector_type_use_case = providers.Factory(
        DeleteSectorTypeUseCase,
        sector_type_repository=sector_type_repository
    )


# Instancia global del contenedor
container = Container() 