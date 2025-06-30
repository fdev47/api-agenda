"""
DTOs para el dominio de ubicaciones
"""
from .requests import (
    CreateCountryRequest, UpdateCountryRequest,
    CreateStateRequest, UpdateStateRequest,
    CreateCityRequest, UpdateCityRequest
)
from .responses import (
    CountryResponse, CountryListResponse,
    StateResponse, StateListResponse,
    CityResponse, CityListResponse
)

__all__ = [
    # Requests
    'CreateCountryRequest', 'UpdateCountryRequest',
    'CreateStateRequest', 'UpdateStateRequest',
    'CreateCityRequest', 'UpdateCityRequest',
    # Responses
    'CountryResponse', 'CountryListResponse',
    'StateResponse', 'StateListResponse',
    'CityResponse', 'CityListResponse'
] 