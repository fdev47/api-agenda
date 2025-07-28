"""
Rutas para locales
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from ...domain.dto.requests.local_requests import CreateLocalRequest, UpdateLocalRequest, LocalFilterRequest
from ...domain.dto.responses.local_responses import (
    LocalResponse, LocalListResponse, LocalCreatedResponse, 
    LocalUpdatedResponse, LocalDeletedResponse
)
from ...infrastructure.container import container
from ...application.use_cases import (
    CreateLocalUseCase, GetLocalUseCase, ListLocalsUseCase,
    UpdateLocalUseCase, DeleteLocalUseCase
)
from ..middleware import auth_middleware

router = APIRouter(tags=["Locals"])


def get_create_local_use_case() -> CreateLocalUseCase:
    return CreateLocalUseCase(
        local_repository=container.local_repository()
    )

def get_get_local_use_case() -> GetLocalUseCase:
    return GetLocalUseCase(
        local_repository=container.local_repository()
    )

def get_list_locals_use_case() -> ListLocalsUseCase:
    return ListLocalsUseCase(
        local_repository=container.local_repository()
    )

def get_update_local_use_case() -> UpdateLocalUseCase:
    return UpdateLocalUseCase(
        local_repository=container.local_repository()
    )

def get_delete_local_use_case() -> DeleteLocalUseCase:
    return DeleteLocalUseCase(
        local_repository=container.local_repository()
    )


@router.post("/", response_model=LocalCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_local(
    request: CreateLocalRequest,
    use_case: CreateLocalUseCase = Depends(get_create_local_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Crear un nuevo local"""
    return await use_case.execute(request)


@router.get("/{local_id}", response_model=LocalResponse)
async def get_local(
    local_id: int,
    use_case: GetLocalUseCase = Depends(get_get_local_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Obtener un local por ID"""
    local = await use_case.execute(local_id)
    if not local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local no encontrado"
        )
    return local


@router.get("/", response_model=LocalListResponse)
async def list_locals(
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    use_case: ListLocalsUseCase = Depends(get_list_locals_use_case),
    current_user=Depends(auth_middleware["require_auth"])
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
async def update_local(
    local_id: int,
    request: UpdateLocalRequest,
    use_case: UpdateLocalUseCase = Depends(get_update_local_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Actualizar un local"""
    local = await use_case.execute(local_id, request)
    if not local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local no encontrado"
        )
    return local


@router.delete("/{local_id}", response_model=LocalDeletedResponse)
async def delete_local(
    local_id: int,
    use_case: DeleteLocalUseCase = Depends(get_delete_local_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Eliminar un local"""
    success = await use_case.execute(local_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local no encontrado"
        )
    return {"success": True, "message": f"Local {local_id} eliminado exitosamente"} 