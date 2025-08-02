"""
Rutas de locals en el API Gateway
"""
from fastapi import APIRouter, Query, Depends, Header
from typing import List, Optional
from ..middleware import auth_middleware
from ...domain.local.dto.responses.local_responses import LocalListResponse
from ...application.local.use_cases.list_locals_use_case import ListLocalsUseCase

router = APIRouter()


@router.get("/", response_model=LocalListResponse)
async def list_locals(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Listar locales disponibles (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = ListLocalsUseCase()
    locals = await use_case.execute(skip=skip, limit=limit, name=name, code=code, is_active=is_active, access_token=access_token)
    
    return LocalListResponse(
        locals=locals,
        total=len(locals),
        limit=limit,
        offset=skip
    ) 