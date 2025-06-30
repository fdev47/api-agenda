"""
Casos de uso del location_service
"""
# Country use cases
from .create_country_use_case import CreateCountryUseCase
from .get_country_use_case import GetCountryByIdUseCase
from .list_countries_use_case import ListCountriesUseCase
from .update_country_use_case import UpdateCountryUseCase
from .delete_country_use_case import DeleteCountryUseCase

# State use cases
from .create_state_use_case import CreateStateUseCase
from .get_state_use_case import GetStateUseCase
from .list_states_use_case import ListStatesUseCase
from .update_state_use_case import UpdateStateUseCase
from .delete_state_use_case import DeleteStateUseCase

# City use cases
from .create_city_use_case import CreateCityUseCase
from .get_city_use_case import GetCityUseCase
from .list_cities_use_case import ListCitiesUseCase
from .update_city_use_case import UpdateCityUseCase
from .delete_city_use_case import DeleteCityUseCase

# Local use cases
from .create_local_use_case import CreateLocalUseCase
from .get_local_use_case import GetLocalUseCase
from .list_locals_use_case import ListLocalsUseCase
from .update_local_use_case import UpdateLocalUseCase
from .delete_local_use_case import DeleteLocalUseCase

# Branch use cases
from .create_branch_use_case import CreateBranchUseCase
from .get_branch_use_case import GetBranchUseCase
from .list_branches_use_case import ListBranchesUseCase
from .update_branch_use_case import UpdateBranchUseCase
from .delete_branch_use_case import DeleteBranchUseCase

__all__ = [
    # Country use cases
    "CreateCountryUseCase",
    "GetCountryByIdUseCase",
    "ListCountriesUseCase",
    "UpdateCountryUseCase",
    "DeleteCountryUseCase",
    
    # State use cases
    "CreateStateUseCase",
    "GetStateUseCase",
    "ListStatesUseCase",
    "UpdateStateUseCase",
    "DeleteStateUseCase",
    
    # City use cases
    "CreateCityUseCase",
    "GetCityUseCase",
    "ListCitiesUseCase",
    "UpdateCityUseCase",
    "DeleteCityUseCase",
    
    # Local use cases
    "CreateLocalUseCase",
    "GetLocalUseCase",
    "ListLocalsUseCase",
    "UpdateLocalUseCase",
    "DeleteLocalUseCase",
    
    # Branch use cases
    "CreateBranchUseCase",
    "GetBranchUseCase",
    "ListBranchesUseCase",
    "UpdateBranchUseCase",
    "DeleteBranchUseCase"
] 