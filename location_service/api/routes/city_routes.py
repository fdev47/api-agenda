"""
Rutas para gestión de ciudades
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from ...domain.dto.requests import CreateCityRequest, UpdateCityRequest
from ...domain.dto.responses import CityResponse, CityListResponse
from ...infrastructure.container import container
from ...application.use_cases import (
    CreateCityUseCase, GetCityUseCase, ListCitiesUseCase,
    UpdateCityUseCase, DeleteCityUseCase
)

router = APIRouter(prefix="/v1/cities", tags=["Cities"])


def get_create_city_use_case() -> CreateCityUseCase:
    return CreateCityUseCase(
        city_repository=container.city_repository(),
        state_repository=container.state_repository()
    )

def get_get_city_use_case() -> GetCityUseCase:
    return GetCityUseCase(
        city_repository=container.city_repository(),
        state_repository=container.state_repository(),
        country_repository=container.country_repository()
    )

def get_list_cities_use_case() -> ListCitiesUseCase:
    return ListCitiesUseCase(
        city_repository=container.city_repository(),
        state_repository=container.state_repository(),
        country_repository=container.country_repository()
    )

def get_update_city_use_case() -> UpdateCityUseCase:
    return UpdateCityUseCase(
        city_repository=container.city_repository(),
        state_repository=container.state_repository()
    )

def get_delete_city_use_case() -> DeleteCityUseCase:
    return DeleteCityUseCase(
        city_repository=container.city_repository()
    )


@router.get("/", response_model=CityListResponse)
async def get_cities(
    state_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    use_case: ListCitiesUseCase = Depends(get_list_cities_use_case)
):
    return await use_case.execute(state_id=state_id, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=CityResponse)
async def get_city(
    city_id: int,
    use_case: GetCityUseCase = Depends(get_get_city_use_case)
):
    return await use_case.execute(city_id)


@router.post("/", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
async def create_city(
    request: CreateCityRequest,
    use_case: CreateCityUseCase = Depends(get_create_city_use_case)
):
    return await use_case.execute(request)


@router.put("/{city_id}", response_model=CityResponse)
async def update_city(
    city_id: int,
    request: UpdateCityRequest,
    use_case: UpdateCityUseCase = Depends(get_update_city_use_case)
):
    return await use_case.execute(city_id, request)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    city_id: int,
    use_case: DeleteCityUseCase = Depends(get_delete_city_use_case)
):
    await use_case.execute(city_id)
    return None 