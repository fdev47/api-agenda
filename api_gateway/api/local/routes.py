"""
Rutas de locals en el API Gateway
"""
from fastapi import APIRouter, Query, Depends, Header, HTTPException, status
from typing import List, Optional
from ..middleware import auth_middleware
from ...domain.local.dto.requests.local_requests import CreateLocalRequest, UpdateLocalRequest
from ...domain.local.dto.responses.local_responses import (
    LocalListResponse, LocalResponse, LocalCreatedResponse, 
    LocalUpdatedResponse, LocalDeletedResponse
)
from ...application.local.use_cases.list_locals_use_case import ListLocalsUseCase
from ...application.local.use_cases.create_local_use_case import CreateLocalUseCase
from ...application.local.use_cases.get_local_use_case import GetLocalUseCase
from ...application.local.use_cases.update_local_use_case import UpdateLocalUseCase
from ...application.local.use_cases.delete_local_use_case import DeleteLocalUseCase

router = APIRouter()


@router.post("/", response_model=LocalCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_local(
    request: CreateLocalRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Crear un nuevo local (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = CreateLocalUseCase()
    result = await use_case.execute(request=request, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el local"
        )
    
    return result


@router.get("/{local_id}", response_model=LocalResponse)
async def get_local(
    local_id: int,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Obtener un local por ID (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = GetLocalUseCase()
    local = await use_case.execute(local_id=local_id, access_token=access_token)
    
    if not local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local no encontrado"
        )
    
    return local


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


@router.put("/{local_id}", response_model=LocalUpdatedResponse)
async def update_local(
    local_id: int,
    request: UpdateLocalRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Actualizar un local (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = UpdateLocalUseCase()
    result = await use_case.execute(local_id=local_id, request=request, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local no encontrado"
        )
    
    return result


@router.delete("/{local_id}", response_model=LocalDeletedResponse)
async def delete_local(
    local_id: int,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Eliminar un local (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = DeleteLocalUseCase()
    result = await use_case.execute(local_id=local_id, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local no encontrado"
        )
    
    return result 