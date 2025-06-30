"""
Interfaces del dominio de ubicaciones
"""
from .country_repository import CountryRepository
from .state_repository import StateRepository
from .city_repository import CityRepository
from .local_repository import LocalRepository
from .branch_repository import BranchRepository

__all__ = [
    "CountryRepository",
    "StateRepository", 
    "CityRepository",
    "LocalRepository",
    "BranchRepository"
] 