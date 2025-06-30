"""
DTOs de responses del dominio de ubicaciones
"""
from .country_responses import (
    CountryResponse,
    CountryListResponse,
    CountryCreatedResponse,
    CountryUpdatedResponse,
    CountryDeletedResponse
)
from .state_responses import (
    StateResponse,
    StateListResponse,
    StateCreatedResponse,
    StateUpdatedResponse,
    StateDeletedResponse
)
from .city_responses import (
    CityResponse,
    CityListResponse,
    CityCreatedResponse,
    CityUpdatedResponse,
    CityDeletedResponse
)
from .local_responses import (
    LocalResponse,
    LocalListResponse,
    LocalCreatedResponse,
    LocalUpdatedResponse,
    LocalDeletedResponse
)
from .branch_responses import (
    BranchResponse,
    BranchListResponse,
    BranchCreatedResponse,
    BranchUpdatedResponse,
    BranchDeletedResponse
)
from .ramp_responses import (
    RampResponse,
    RampListResponse,
    RampCreatedResponse,
    RampUpdatedResponse,
    RampDeletedResponse
)
from .sector_responses import (
    SectorResponse,
    SectorListResponse,
    SectorCreatedResponse,
    SectorUpdatedResponse,
    SectorDeletedResponse
)
from .error_responses import (
    ErrorResponse,
    ValidationErrorResponse
)

__all__ = [
    # Country responses
    "CountryResponse",
    "CountryListResponse",
    "CountryCreatedResponse",
    "CountryUpdatedResponse",
    "CountryDeletedResponse",
    # State responses
    "StateResponse",
    "StateListResponse",
    "StateCreatedResponse",
    "StateUpdatedResponse",
    "StateDeletedResponse",
    # City responses
    "CityResponse",
    "CityListResponse",
    "CityCreatedResponse",
    "CityUpdatedResponse",
    "CityDeletedResponse",
    # Local responses
    "LocalResponse",
    "LocalListResponse",
    "LocalCreatedResponse",
    "LocalUpdatedResponse",
    "LocalDeletedResponse",
    # Branch responses
    "BranchResponse",
    "BranchListResponse",
    "BranchCreatedResponse",
    "BranchUpdatedResponse",
    "BranchDeletedResponse",
    # Ramp responses
    "RampResponse",
    "RampListResponse",
    "RampCreatedResponse",
    "RampUpdatedResponse",
    "RampDeletedResponse",
    # Sector responses
    "SectorResponse",
    "SectorListResponse",
    "SectorCreatedResponse",
    "SectorUpdatedResponse",
    "SectorDeletedResponse",
    # Error responses
    "ErrorResponse",
    "ValidationErrorResponse"
] 