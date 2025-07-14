"""
Rutas para gestión de países
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ...domain.dto.requests import CreateCountryRequest, UpdateCountryRequest
from ...domain.dto.responses import CountryResponse, CountryListResponse
from ...infrastructure.container import container
from ...application.use_cases import (
    CreateCountryUseCase, GetCountryByIdUseCase, ListCountriesUseCase,
    UpdateCountryUseCase, DeleteCountryUseCase
)

router = APIRouter(prefix="/countries", tags=["Countries"])


def get_create_country_use_case() -> CreateCountryUseCase:
    return CreateCountryUseCase(
        country_repository=container.country_repository()
    )

def get_get_country_use_case() -> GetCountryByIdUseCase:
    return GetCountryByIdUseCase(
        country_repository=container.country_repository()
    )

def get_list_countries_use_case() -> ListCountriesUseCase:
    return ListCountriesUseCase(
        country_repository=container.country_repository()
    )

def get_update_country_use_case() -> UpdateCountryUseCase:
    return UpdateCountryUseCase(
        country_repository=container.country_repository()
    )

def get_delete_country_use_case() -> DeleteCountryUseCase:
    return DeleteCountryUseCase(
        country_repository=container.country_repository(),
        state_repository=container.state_repository()
    )


@router.get("/", response_model=CountryListResponse)
async def get_countries(
    skip: int = 0,
    limit: int = 100,
    use_case: ListCountriesUseCase = Depends(get_list_countries_use_case)
):
    return await use_case.execute(skip=skip, limit=limit)


@router.get("/{country_id}", response_model=CountryResponse)
async def get_country(
    country_id: int,
    use_case: GetCountryByIdUseCase = Depends(get_get_country_use_case)
):
    return await use_case.execute(country_id)


@router.post("/", response_model=CountryResponse, status_code=status.HTTP_201_CREATED)
async def create_country(
    request: CreateCountryRequest,
    use_case: CreateCountryUseCase = Depends(get_create_country_use_case)
):
    return await use_case.execute(request)


@router.put("/{country_id}", response_model=CountryResponse)
async def update_country(
    country_id: int,
    request: UpdateCountryRequest,
    use_case: UpdateCountryUseCase = Depends(get_update_country_use_case)
):
    return await use_case.execute(country_id, request)


@router.delete("/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(
    country_id: int,
    use_case: DeleteCountryUseCase = Depends(get_delete_country_use_case)
):
    await use_case.execute(country_id)
    return None 