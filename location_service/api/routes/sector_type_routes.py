"""
Rutas para gestión de tipos de sector
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from ...domain.dto.requests import CreateSectorTypeRequest, UpdateSectorTypeRequest
from ...domain.dto.responses import SectorTypeResponse, SectorTypeListResponse
from ...infrastructure.container import container
from ...application.use_cases import (
    CreateSectorTypeUseCase, GetSectorTypeUseCase, ListSectorTypesUseCase,
    UpdateSectorTypeUseCase, DeleteSectorTypeUseCase
)
from ...domain.dto.requests import SectorTypeFilterRequest
from ..middleware import auth_middleware

router = APIRouter(tags=["Sector Types"])


def get_create_sector_type_use_case() -> CreateSectorTypeUseCase:
    return CreateSectorTypeUseCase(
        sector_type_repository=container.sector_type_repository()
    )

def get_get_sector_type_use_case() -> GetSectorTypeUseCase:
    return GetSectorTypeUseCase(
        sector_type_repository=container.sector_type_repository()
    )

def get_list_sector_types_use_case() -> ListSectorTypesUseCase:
    return ListSectorTypesUseCase(
        sector_type_repository=container.sector_type_repository()
    )

def get_update_sector_type_use_case() -> UpdateSectorTypeUseCase:
    return UpdateSectorTypeUseCase(
        sector_type_repository=container.sector_type_repository()
    )

def get_delete_sector_type_use_case() -> DeleteSectorTypeUseCase:
    return DeleteSectorTypeUseCase(
        sector_type_repository=container.sector_type_repository()
    )


@router.get("/", response_model=SectorTypeListResponse)
async def get_sector_types(
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    use_case: ListSectorTypesUseCase = Depends(get_list_sector_types_use_case)
):
    """Listar tipos de sector con filtros"""
    filter_request = SectorTypeFilterRequest(
        name=name,
        code=code,
        limit=limit,
        offset=offset
    )
    return await use_case.execute(filter_request)


@router.get("/{sector_type_id}", response_model=SectorTypeResponse)
async def get_sector_type(
    sector_type_id: int,
    use_case: GetSectorTypeUseCase = Depends(get_get_sector_type_use_case)
):
    sector_type = await use_case.execute(sector_type_id)
    if not sector_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de sector no encontrado"
        )
    return sector_type


@router.post("/", response_model=SectorTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_sector_type(
    request: CreateSectorTypeRequest,
    use_case: CreateSectorTypeUseCase = Depends(get_create_sector_type_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    return await use_case.execute(request)


@router.put("/{sector_type_id}", response_model=SectorTypeResponse)
async def update_sector_type(
    sector_type_id: int,
    request: UpdateSectorTypeRequest,
    use_case: UpdateSectorTypeUseCase = Depends(get_update_sector_type_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    sector_type = await use_case.execute(sector_type_id, request)
    if not sector_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de sector no encontrado"
        )
    return sector_type


@router.delete("/{sector_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sector_type(
    sector_type_id: int,
    use_case: DeleteSectorTypeUseCase = Depends(get_delete_sector_type_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    success = await use_case.execute(sector_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de sector no encontrado"
        ) 