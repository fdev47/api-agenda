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

# Sector use cases
from .create_sector_use_case import CreateSectorUseCase
from .get_sector_use_case import GetSectorUseCase
from .list_sectors_use_case import ListSectorsUseCase
from .update_sector_use_case import UpdateSectorUseCase
from .delete_sector_use_case import DeleteSectorUseCase

# Sector Type use cases
from .create_sector_type_use_case import CreateSectorTypeUseCase
from .get_sector_type_use_case import GetSectorTypeUseCase
from .list_sector_types_use_case import ListSectorTypesUseCase
from .update_sector_type_use_case import UpdateSectorTypeUseCase
from .delete_sector_type_use_case import DeleteSectorTypeUseCase

# MeasurementUnit use cases
from .create_measurement_unit_use_case import CreateMeasurementUnitUseCase
from .get_measurement_unit_use_case import GetMeasurementUnitUseCase
from .list_measurement_units_use_case import ListMeasurementUnitsUseCase
from .update_measurement_unit_use_case import UpdateMeasurementUnitUseCase
from .delete_measurement_unit_use_case import DeleteMeasurementUnitUseCase

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
    "DeleteBranchUseCase",
    
    # Sector use cases
    "CreateSectorUseCase",
    "GetSectorUseCase",
    "ListSectorsUseCase",
    "UpdateSectorUseCase",
    "DeleteSectorUseCase",
    
    # Sector Type use cases
    "CreateSectorTypeUseCase",
    "GetSectorTypeUseCase",
    "ListSectorTypesUseCase",
    "UpdateSectorTypeUseCase",
    "DeleteSectorTypeUseCase",
    
    # MeasurementUnit use cases
    "CreateMeasurementUnitUseCase",
    "GetMeasurementUnitUseCase",
    "ListMeasurementUnitsUseCase",
    "UpdateMeasurementUnitUseCase",
    "DeleteMeasurementUnitUseCase"
] 