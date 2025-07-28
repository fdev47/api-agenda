"""
Rutas para sucursales
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from ...domain.dto.requests.branch_requests import CreateBranchRequest, UpdateBranchRequest, BranchFilterRequest
from ...domain.dto.responses.branch_responses import (
    BranchResponse, BranchListResponse, BranchCreatedResponse, 
    BranchUpdatedResponse, BranchDeletedResponse
)
from ...infrastructure.container import container
from ...application.use_cases import (
    CreateBranchUseCase, GetBranchUseCase, ListBranchesUseCase,
    UpdateBranchUseCase, DeleteBranchUseCase
)
from ..middleware import auth_middleware

router = APIRouter(tags=["Branches"])


def get_create_branch_use_case() -> CreateBranchUseCase:
    return CreateBranchUseCase(
        branch_repository=container.branch_repository(),
        local_repository=container.local_repository(),
        country_repository=container.country_repository(),
        state_repository=container.state_repository(),
        city_repository=container.city_repository()
    )

def get_get_branch_use_case() -> GetBranchUseCase:
    return GetBranchUseCase(
        branch_repository=container.branch_repository(),
        local_repository=container.local_repository(),
        country_repository=container.country_repository(),
        state_repository=container.state_repository(),
        city_repository=container.city_repository()
    )

def get_list_branches_use_case() -> ListBranchesUseCase:
    return ListBranchesUseCase(
        branch_repository=container.branch_repository(),
        local_repository=container.local_repository(),
        country_repository=container.country_repository(),
        state_repository=container.state_repository(),
        city_repository=container.city_repository()
    )

def get_update_branch_use_case() -> UpdateBranchUseCase:
    return UpdateBranchUseCase(
        branch_repository=container.branch_repository(),
        local_repository=container.local_repository(),
        country_repository=container.country_repository(),
        state_repository=container.state_repository(),
        city_repository=container.city_repository()
    )

def get_delete_branch_use_case() -> DeleteBranchUseCase:
    return DeleteBranchUseCase(
        branch_repository=container.branch_repository()
    )


@router.post("/", response_model=BranchCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_branch(
    request: CreateBranchRequest,
    use_case: CreateBranchUseCase = Depends(get_create_branch_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Crear una nueva sucursal"""
    return await use_case.execute(request)


@router.get("/{branch_id}", response_model=BranchResponse)
async def get_branch(
    branch_id: int,
    use_case: GetBranchUseCase = Depends(get_get_branch_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Obtener una sucursal por ID"""
    branch = await use_case.execute(branch_id)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sucursal no encontrada"
        )
    return branch


@router.get("/", response_model=BranchListResponse)
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
    use_case: ListBranchesUseCase = Depends(get_list_branches_use_case),
    current_user=Depends(auth_middleware["require_auth"])
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
async def update_branch(
    branch_id: int,
    request: UpdateBranchRequest,
    use_case: UpdateBranchUseCase = Depends(get_update_branch_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Actualizar una sucursal"""
    branch = await use_case.execute(branch_id, request)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sucursal no encontrada"
        )
    return branch


@router.delete("/{branch_id}", response_model=BranchDeletedResponse)
async def delete_branch(
    branch_id: int,
    use_case: DeleteBranchUseCase = Depends(get_delete_branch_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Eliminar una sucursal"""
    success = await use_case.execute(branch_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sucursal no encontrada"
        )
    return {"success": True, "message": f"Sucursal {branch_id} eliminada exitosamente"} 