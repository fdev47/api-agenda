"""
Rutas de branches en el API Gateway
"""
from fastapi import APIRouter, Query, Depends, Header
from typing import List, Optional
from ..middleware import auth_middleware
from ...domain.branch.dto.responses.branch_responses import BranchListResponse
from ...application.branch.use_cases.list_branches_use_case import ListBranchesUseCase

router = APIRouter()


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