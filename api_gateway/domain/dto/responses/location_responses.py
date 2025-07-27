"""
DTOs de respuestas para location en el API Gateway
"""
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class CountryResponse(BaseModel):
    """DTO para respuesta de país"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    code: Optional[str] = None
    is_active: bool

class StateResponse(BaseModel):
    """DTO para respuesta de estado/provincia"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    code: Optional[str] = None
    country_id: int
    is_active: bool

class CityResponse(BaseModel):
    """DTO para respuesta de ciudad"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    code: Optional[str] = None
    state_id: int
    is_active: bool

class CountryListResponse(BaseModel):
    """DTO para respuesta de lista de países"""
    countries: List[CountryResponse]
    total: int
    skip: int
    limit: int

class StateListResponse(BaseModel):
    """DTO para respuesta de lista de estados"""
    states: List[StateResponse]
    total: int
    skip: int
    limit: int

class CityListResponse(BaseModel):
    """DTO para respuesta de lista de ciudades"""
    cities: List[CityResponse]
    total: int
    skip: int
    limit: int 