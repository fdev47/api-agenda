"""
Rutas de location en el API Gateway
"""
from fastapi import APIRouter, Query, Depends, Header
from typing import List, Optional
from ..middleware import auth_middleware
from ...domain.location.dto.responses.location_responses import (
    CountryListResponse, 
    StateListResponse, 
    CityListResponse,
    MeasurementUnitListResponse,
    SectorTypeListResponse,
    LocalListResponse
)
from ...application.location.use_cases.list_countries_use_case import ListCountriesUseCase
from ...application.location.use_cases.list_states_use_case import ListStatesUseCase
from ...application.location.use_cases.list_cities_use_case import ListCitiesUseCase
from ...application.location.use_cases.list_measurement_units_use_case import ListMeasurementUnitsUseCase
from ...application.location.use_cases.list_sector_types_use_case import ListSectorTypesUseCase
from ...application.location.use_cases.list_locals_use_case import ListLocalsUseCase

router = APIRouter()

@router.get("/countries", response_model=CountryListResponse)
async def list_countries(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros")
):
    """
    Listar países disponibles
    """
    use_case = ListCountriesUseCase()
    countries = await use_case.execute(skip=skip, limit=limit)
    
    return CountryListResponse(
        countries=countries,
        total=len(countries),
        skip=skip,
        limit=limit
    )

@router.get("/states", response_model=StateListResponse)
async def list_states(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    country_id: Optional[str] = Query(None, description="ID del país para filtrar estados")
):
    """
    Listar estados/provincias disponibles
    """
    use_case = ListStatesUseCase()
    states = await use_case.execute(skip=skip, limit=limit, country_id=country_id)
    
    return StateListResponse(
        states=states,
        total=len(states),
        skip=skip,
        limit=limit
    )

@router.get("/cities", response_model=CityListResponse)
async def list_cities(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    state_id: Optional[str] = Query(None, description="ID del estado para filtrar ciudades")
):
    """
    Listar ciudades disponibles
    """
    use_case = ListCitiesUseCase()
    cities = await use_case.execute(skip=skip, limit=limit, state_id=state_id)
    
    return CityListResponse(
        cities=cities,
        total=len(cities),
        skip=skip,
        limit=limit
    )

@router.get("/measurement-units", response_model=MeasurementUnitListResponse)
async def list_measurement_units(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo")
):
    """
    Listar unidades de medida disponibles
    """
    use_case = ListMeasurementUnitsUseCase()
    measurement_units = await use_case.execute(skip=skip, limit=limit, name=name, code=code, is_active=is_active)
    
    return MeasurementUnitListResponse(
        items=measurement_units,
        total=len(measurement_units),
        limit=limit,
        offset=skip
    )

@router.get("/sector-types", response_model=SectorTypeListResponse)
async def list_sector_types(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo")
):
    """
    Listar tipos de sector disponibles
    """
    use_case = ListSectorTypesUseCase()
    sector_types = await use_case.execute(skip=skip, limit=limit, name=name, code=code, is_active=is_active)
    
    return SectorTypeListResponse(
        sector_types=sector_types,
        total=len(sector_types),
        page=1,  # Por defecto página 1
        size=limit
    )


@router.get("/locals", response_model=LocalListResponse)
async def list_locals(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Listar locales disponibles (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = ListLocalsUseCase()
    locals = await use_case.execute(skip=skip, limit=limit, name=name, code=code, is_active=is_active, access_token=access_token)
    
    return LocalListResponse(
        locals=locals,
        total=len(locals),
        limit=limit,
        offset=skip
    )
