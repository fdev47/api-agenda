"""
Rutas para gestión de ciudades
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ...domain.dto.requests import CreateCityRequest, UpdateCityRequest, CityFilterRequest
from ...domain.dto.responses import CityResponse, CityListResponse
from ...infrastructure.container import container
from ...application.use_cases import (
    CreateCityUseCase, GetCityUseCase, ListCitiesUseCase,
    UpdateCityUseCase, DeleteCityUseCase
)
from ..middleware import auth_middleware

router = APIRouter(tags=["Cities"])


def get_create_city_use_case() -> CreateCityUseCase:
    return container.create_city_use_case()

def get_get_city_use_case() -> GetCityUseCase:
    return container.get_city_use_case()

def get_list_cities_use_case() -> ListCitiesUseCase:
    return container.list_cities_use_case()

def get_update_city_use_case() -> UpdateCityUseCase:
    return container.update_city_use_case()

def get_delete_city_use_case() -> DeleteCityUseCase:
    return container.delete_city_use_case()


@router.get("/", response_model=CityListResponse)
async def get_cities(
    skip: int = 0,
    limit: int = 100,
    use_case: ListCitiesUseCase = Depends(get_list_cities_use_case)
):
    filter_request = CityFilterRequest(skip=skip, limit=limit)
    return await use_case.execute(filter_request)


@router.get("/{city_id}", response_model=CityResponse)
async def get_city(
    city_id: int,
    use_case: GetCityUseCase = Depends(get_get_city_use_case)
):
    city = await use_case.execute(city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad no encontrada"
        )
    return city


@router.post("/", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
async def create_city(
    request: CreateCityRequest,
    use_case: CreateCityUseCase = Depends(get_create_city_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    return await use_case.execute(request)


@router.put("/{city_id}", response_model=CityResponse)
async def update_city(
    city_id: int,
    request: UpdateCityRequest,
    use_case: UpdateCityUseCase = Depends(get_update_city_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    city = await use_case.execute(city_id, request)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad no encontrada"
        )
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    city_id: int,
    use_case: DeleteCityUseCase = Depends(get_delete_city_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    success = await use_case.execute(city_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad no encontrada"
        )
    return None 