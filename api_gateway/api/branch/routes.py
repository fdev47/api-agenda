"""
Rutas de branches en el API Gateway
"""
from fastapi import APIRouter, Query, Depends, Header, HTTPException, status
from typing import List, Optional
from ..middleware import auth_middleware
from ...domain.branch.dto.requests.branch_requests import CreateBranchRequest, UpdateBranchRequest
from ...domain.branch.dto.responses.branch_responses import (
    BranchListResponse, BranchResponse, BranchCreatedResponse, 
    BranchUpdatedResponse, BranchDeletedResponse
)
from ...application.branch.use_cases.list_branches_use_case import ListBranchesUseCase
from ...application.branch.use_cases.create_branch_use_case import CreateBranchUseCase
from ...application.branch.use_cases.get_branch_use_case import GetBranchUseCase
from ...application.branch.use_cases.update_branch_use_case import UpdateBranchUseCase
from ...application.branch.use_cases.delete_branch_use_case import DeleteBranchUseCase

router = APIRouter()


@router.post("/", response_model=BranchCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_branch(
    request: CreateBranchRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Crear una nueva sucursal (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = CreateBranchUseCase()
    result = await use_case.execute(request=request, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la sucursal"
        )
    
    return result


@router.get("/{branch_id}", response_model=BranchResponse)
async def get_branch(
    branch_id: int,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Obtener una sucursal por ID (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = GetBranchUseCase()
    branch = await use_case.execute(branch_id=branch_id, access_token=access_token)
    
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sucursal no encontrada"
        )
    
    return branch


@router.get("/", response_model=BranchListResponse)
async def list_branches(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    local_id: Optional[int] = Query(None, description="Filtrar por local"),
    country_id: Optional[int] = Query(None, description="Filtrar por país"),
    state_id: Optional[int] = Query(None, description="Filtrar por estado"),
    city_id: Optional[int] = Query(None, description="Filtrar por ciudad"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Listar sucursales disponibles (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = ListBranchesUseCase()
    branches = await use_case.execute(skip=skip, limit=limit, name=name, code=code, local_id=local_id, country_id=country_id, state_id=state_id, city_id=city_id, is_active=is_active, access_token=access_token)
    
    return BranchListResponse(
        branches=branches,
        total=len(branches),
        limit=limit,
        offset=skip
    )


@router.put("/{branch_id}", response_model=BranchUpdatedResponse)
async def update_branch(
    branch_id: int,
    request: UpdateBranchRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Actualizar una sucursal (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = UpdateBranchUseCase()
    result = await use_case.execute(branch_id=branch_id, request=request, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sucursal no encontrada"
        )
    
    return result


@router.delete("/{branch_id}", response_model=BranchDeletedResponse)
async def delete_branch(
    branch_id: int,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Eliminar una sucursal (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = DeleteBranchUseCase()
    result = await use_case.execute(branch_id=branch_id, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sucursal no encontrada"
        )
    
    return result 