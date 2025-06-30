"""
Rutas para sucursales
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from dependency_injector.wiring import inject, Provide

from ...infrastructure.container import Container
from ...domain.dto.requests.branch_requests import CreateBranchRequest, UpdateBranchRequest, BranchFilterRequest
from ...domain.dto.responses.branch_responses import (
    BranchResponse, BranchListResponse, BranchCreatedResponse, 
    BranchUpdatedResponse, BranchDeletedResponse
)

router = APIRouter(prefix="/branches", tags=["Sucursales"])


@router.post("/", response_model=BranchCreatedResponse, status_code=201)
@inject
async def create_branch(
    request: CreateBranchRequest,
    use_case=Depends(Provide[Container.create_branch_use_case])
):
    """Crear una nueva sucursal"""
    return await use_case.execute(request)


@router.get("/{branch_id}", response_model=BranchResponse)
@inject
async def get_branch(
    branch_id: int,
    use_case=Depends(Provide[Container.get_branch_use_case])
):
    """Obtener una sucursal por ID"""
    return await use_case.execute(branch_id)


@router.get("/", response_model=BranchListResponse)
@inject
async def list_branches(
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    local_id: Optional[int] = Query(None, description="Filtrar por local"),
    country_id: Optional[int] = Query(None, description="Filtrar por país"),
    state_id: Optional[int] = Query(None, description="Filtrar por estado"),
    city_id: Optional[int] = Query(None, description="Filtrar por ciudad"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    use_case=Depends(Provide[Container.list_branches_use_case])
):
    """Listar sucursales con filtros"""
    filter_request = BranchFilterRequest(
        name=name,
        code=code,
        local_id=local_id,
        country_id=country_id,
        state_id=state_id,
        city_id=city_id,
        is_active=is_active,
        limit=limit,
        offset=offset
    )
    
    return await use_case.execute(filter_request)


@router.put("/{branch_id}", response_model=BranchUpdatedResponse)
@inject
async def update_branch(
    branch_id: int,
    request: UpdateBranchRequest,
    use_case=Depends(Provide[Container.update_branch_use_case])
):
    """Actualizar una sucursal"""
    return await use_case.execute(branch_id, request)


@router.delete("/{branch_id}", response_model=BranchDeletedResponse)
@inject
async def delete_branch(
    branch_id: int,
    use_case=Depends(Provide[Container.delete_branch_use_case])
):
    """Eliminar una sucursal"""
    return await use_case.execute(branch_id) 