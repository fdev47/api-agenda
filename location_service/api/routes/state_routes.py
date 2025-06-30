"""
Rutas para gestión de estados
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from ...domain.dto.requests import CreateStateRequest, UpdateStateRequest
from ...domain.dto.responses import StateResponse, StateListResponse
from ...infrastructure.container import container
from ...application.use_cases import (
    CreateStateUseCase, GetStateUseCase, ListStatesUseCase,
    UpdateStateUseCase, DeleteStateUseCase
)

router = APIRouter(prefix="/v1/states", tags=["States"])


def get_create_state_use_case() -> CreateStateUseCase:
    return CreateStateUseCase(
        state_repository=container.state_repository(),
        country_repository=container.country_repository()
    )

def get_get_state_use_case() -> GetStateUseCase:
    return GetStateUseCase(
        state_repository=container.state_repository(),
        country_repository=container.country_repository()
    )

def get_list_states_use_case() -> ListStatesUseCase:
    return ListStatesUseCase(
        state_repository=container.state_repository(),
        country_repository=container.country_repository()
    )

def get_update_state_use_case() -> UpdateStateUseCase:
    return UpdateStateUseCase(
        state_repository=container.state_repository(),
        country_repository=container.country_repository()
    )

def get_delete_state_use_case() -> DeleteStateUseCase:
    return DeleteStateUseCase(
        state_repository=container.state_repository(),
        city_repository=container.city_repository()
    )


@router.get("/", response_model=StateListResponse)
async def get_states(
    country_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    use_case: ListStatesUseCase = Depends(get_list_states_use_case)
):
    return await use_case.execute(country_id=country_id, skip=skip, limit=limit)


@router.get("/{state_id}", response_model=StateResponse)
async def get_state(
    state_id: int,
    use_case: GetStateUseCase = Depends(get_get_state_use_case)
):
    return await use_case.execute(state_id)


@router.post("/", response_model=StateResponse, status_code=status.HTTP_201_CREATED)
async def create_state(
    request: CreateStateRequest,
    use_case: CreateStateUseCase = Depends(get_create_state_use_case)
):
    return await use_case.execute(request)


@router.put("/{state_id}", response_model=StateResponse)
async def update_state(
    state_id: int,
    request: UpdateStateRequest,
    use_case: UpdateStateUseCase = Depends(get_update_state_use_case)
):
    return await use_case.execute(state_id, request)


@router.delete("/{state_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_state(
    state_id: int,
    use_case: DeleteStateUseCase = Depends(get_delete_state_use_case)
):
    await use_case.execute(state_id)
    return None 