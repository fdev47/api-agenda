"""
Rutas para gestión de estados
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import List

from ...domain.dto.requests import CreateStateRequest, UpdateStateRequest, StateFilterRequest
from ...domain.dto.responses import StateResponse, StateListResponse
from ...infrastructure.container import container
from ...application.use_cases import (
    CreateStateUseCase, GetStateUseCase, ListStatesUseCase,
    UpdateStateUseCase, DeleteStateUseCase
)
from ..middleware import auth_middleware

router = APIRouter(tags=["States"])


def get_create_state_use_case() -> CreateStateUseCase:
    return container.create_state_use_case()

def get_get_state_use_case() -> GetStateUseCase:
    return container.get_state_use_case()

def get_list_states_use_case() -> ListStatesUseCase:
    return container.list_states_use_case()

def get_update_state_use_case() -> UpdateStateUseCase:
    return container.update_state_use_case()

def get_delete_state_use_case() -> DeleteStateUseCase:
    return container.delete_state_use_case()


@router.get("/", response_model=StateListResponse)
async def get_states(
    skip: int = 0,
    limit: int = 100,
    use_case: ListStatesUseCase = Depends(get_list_states_use_case)
):
    filter_request = StateFilterRequest(skip=skip, limit=limit)
    return await use_case.execute(filter_request)


@router.get("/{state_id}", response_model=StateResponse)
async def get_state(
    state_id: int,
    use_case: GetStateUseCase = Depends(get_get_state_use_case)
):
    state = await use_case.execute(state_id)
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estado no encontrado"
        )
    return state


@router.post("/", response_model=StateResponse, status_code=status.HTTP_201_CREATED)
async def create_state(
    request: CreateStateRequest,
    use_case: CreateStateUseCase = Depends(get_create_state_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    return await use_case.execute(request)


@router.put("/{state_id}", response_model=StateResponse)
async def update_state(
    state_id: int,
    request: UpdateStateRequest,
    use_case: UpdateStateUseCase = Depends(get_update_state_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    state = await use_case.execute(state_id, request)
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estado no encontrado"
        )
    return state


@router.delete("/{state_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_state(
    state_id: int,
    use_case: DeleteStateUseCase = Depends(get_delete_state_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    success = await use_case.execute(state_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estado no encontrado"
        )
    return None 