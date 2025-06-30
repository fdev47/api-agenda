"""
DTOs de requests del dominio de ubicaciones
"""
from .country_requests import (
    CreateCountryRequest,
    UpdateCountryRequest,
    CountryFilterRequest
)
from .state_requests import (
    CreateStateRequest,
    UpdateStateRequest,
    StateFilterRequest
)
from .city_requests import (
    CreateCityRequest,
    UpdateCityRequest,
    CityFilterRequest
)
from .local_requests import (
    CreateLocalRequest,
    UpdateLocalRequest,
    LocalFilterRequest
)
from .branch_requests import (
    CreateBranchRequest,
    UpdateBranchRequest,
    BranchFilterRequest
)
from .ramp_requests import (
    CreateRampRequest,
    UpdateRampRequest,
    RampFilterRequest
)
from .sector_requests import (
    CreateSectorRequest,
    UpdateSectorRequest,
    SectorFilterRequest
)
from .sector_type_requests import (
    CreateSectorTypeRequest,
    UpdateSectorTypeRequest,
    SectorTypeFilterRequest
)

__all__ = [
    # Country requests
    "CreateCountryRequest",
    "UpdateCountryRequest",
    "CountryFilterRequest",
    # State requests
    "CreateStateRequest",
    "UpdateStateRequest",
    "StateFilterRequest",
    # City requests
    "CreateCityRequest",
    "UpdateCityRequest",
    "CityFilterRequest",
    # Local requests
    "CreateLocalRequest",
    "UpdateLocalRequest",
    "LocalFilterRequest",
    # Branch requests
    "CreateBranchRequest",
    "UpdateBranchRequest",
    "BranchFilterRequest",
    # Ramp requests
    "CreateRampRequest",
    "UpdateRampRequest",
    "RampFilterRequest",
    # Sector requests
    "CreateSectorRequest",
    "UpdateSectorRequest",
    "SectorFilterRequest",
    # SectorType requests
    "CreateSectorTypeRequest",
    "UpdateSectorTypeRequest",
    "SectorTypeFilterRequest"
] 