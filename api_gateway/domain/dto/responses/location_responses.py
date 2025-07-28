"""
DTOs de respuestas para location en el API Gateway
"""
from pydantic import BaseModel, ConfigDict, Field
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

class MeasurementUnitResponse(BaseModel):
    """Response para una unidad de medida"""
    id: int = Field(..., description="ID de la unidad de medida")
    name: str = Field(..., description="Nombre de la unidad de medida")
    code: str = Field(..., description="Código de la unidad de medida")
    description: Optional[str] = Field(None, description="Descripción de la unidad de medida")
    is_active: bool = Field(..., description="Estado activo de la unidad de medida")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

    class Config:
        from_attributes = True

class SectorTypeResponse(BaseModel):
    """DTO para respuesta de tipo de sector"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID del tipo de sector")
    name: str = Field(..., description="Nombre del tipo de sector")
    code: str = Field(..., description="Código del tipo de sector")
    description: Optional[str] = Field(None, description="Descripción del tipo de sector")
    is_active: bool = Field(..., description="Estado activo del tipo de sector")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

class MeasurementUnitListResponse(BaseModel):
    """Response para lista de unidades de medida"""
    items: List[MeasurementUnitResponse] = Field(..., description="Lista de unidades de medida")
    total: int = Field(..., description="Total de unidades de medida")
    limit: int = Field(..., description="Límite de resultados")
    offset: int = Field(..., description="Offset para paginación")

class SectorTypeListResponse(BaseModel):
    """DTO para lista de tipos de sector"""
    sector_types: List[SectorTypeResponse] = Field(..., description="Lista de tipos de sector")
    total: int = Field(..., description="Total de tipos de sector")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de la página")


class LocalResponse(BaseModel):
    """Response para un local"""
    id: int = Field(..., description="ID del local")
    name: str = Field(..., description="Nombre del local")
    code: str = Field(..., description="Código único del local")
    description: Optional[str] = Field(None, description="Descripción del local")
    phone: Optional[str] = Field(None, description="Teléfono del local")
    email: Optional[str] = Field(None, description="Email del local")
    is_active: bool = Field(..., description="Estado activo del local")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True


class LocalListResponse(BaseModel):
    """Response para lista de locales"""
    locals: List[LocalResponse] = Field(..., description="Lista de locales")
    total: int = Field(..., description="Total de locales")
    limit: int = Field(..., description="Límite de resultados")
    offset: int = Field(..., description="Offset para paginación") 