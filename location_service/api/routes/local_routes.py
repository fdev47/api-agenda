"""
Rutas para locales
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from dependency_injector.wiring import inject, Provide

from ...infrastructure.container import Container
from ...domain.dto.requests.local_requests import CreateLocalRequest, UpdateLocalRequest, LocalFilterRequest
from ...domain.dto.responses.local_responses import (
    LocalResponse, LocalListResponse, LocalCreatedResponse, 
    LocalUpdatedResponse, LocalDeletedResponse
)

router = APIRouter(prefix="/locals", tags=["Locales"])


@router.post("/", response_model=LocalCreatedResponse, status_code=201)
@inject
async def create_local(
    request: CreateLocalRequest,
    use_case=Depends(Provide[Container.create_local_use_case])
):
    """Crear un nuevo local"""
    return await use_case.execute(request)


@router.get("/{local_id}", response_model=LocalResponse)
@inject
async def get_local(
    local_id: int,
    use_case=Depends(Provide[Container.get_local_use_case])
):
    """Obtener un local por ID"""
    return await use_case.execute(local_id)


@router.get("/", response_model=LocalListResponse)
@inject
async def list_locals(
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    use_case=Depends(Provide[Container.list_locals_use_case])
):
    """Listar locales con filtros"""
    filter_request = LocalFilterRequest(
        name=name,
        code=code,
        is_active=is_active,
        limit=limit,
        offset=offset
    )
    
    return await use_case.execute(filter_request)


@router.put("/{local_id}", response_model=LocalUpdatedResponse)
@inject
async def update_local(
    local_id: int,
    request: UpdateLocalRequest,
    use_case=Depends(Provide[Container.update_local_use_case])
):
    """Actualizar un local"""
    return await use_case.execute(local_id, request)


@router.delete("/{local_id}", response_model=LocalDeletedResponse)
@inject
async def delete_local(
    local_id: int,
    use_case=Depends(Provide[Container.delete_local_use_case])
):
    """Eliminar un local"""
    return await use_case.execute(local_id) 