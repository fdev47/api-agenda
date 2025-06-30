"""
Excepciones del dominio de ubicaciones
"""
from .location_exceptions import (
    LocationDomainException,
    CountryNotFoundException,
    StateNotFoundException,
    CityNotFoundException,
    CountryAlreadyExistsException,
    StateAlreadyExistsException,
    CityAlreadyExistsException,
    LocationValidationException
)
from .local_exceptions import (
    LocalNotFoundException,
    LocalAlreadyExistsException,
    LocalValidationException
)
from .branch_exceptions import (
    BranchNotFoundException,
    BranchAlreadyExistsException,
    BranchValidationException
)
from .ramp_exceptions import (
    RampNotFoundException,
    RampAlreadyExistsException,
    RampValidationException
)
from .sector_exceptions import (
    SectorNotFoundException,
    SectorAlreadyExistsException,
    SectorValidationException
)
from .sector_type_exceptions import (
    SectorTypeNotFoundException,
    SectorTypeAlreadyExistsException,
    SectorTypeValidationException
)

# Alias para compatibilidad
LocationException = LocationDomainException

__all__ = [
    # Location exceptions
    "LocationDomainException",
    "LocationException",  # Alias
    "CountryNotFoundException",
    "StateNotFoundException", 
    "CityNotFoundException",
    "CountryAlreadyExistsException",
    "StateAlreadyExistsException",
    "CityAlreadyExistsException",
    "LocationValidationException",
    # Local exceptions
    "LocalNotFoundException",
    "LocalAlreadyExistsException",
    "LocalValidationException",
    # Branch exceptions
    "BranchNotFoundException",
    "BranchAlreadyExistsException",
    "BranchValidationException",
    # Ramp exceptions
    "RampNotFoundException",
    "RampAlreadyExistsException",
    "RampValidationException",
    # Sector exceptions
    "SectorNotFoundException",
    "SectorAlreadyExistsException",
    "SectorValidationException",
    # Sector Type exceptions
    "SectorTypeNotFoundException",
    "SectorTypeAlreadyExistsException",
    "SectorTypeValidationException"
] 