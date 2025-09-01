"""
Rutas para gestión de sectores
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from ...domain.dto.requests.sector_requests import CreateSectorRequest, UpdateSectorRequest, SectorFilterRequest
from ...domain.dto.responses.sector_responses import SectorResponse, SectorListResponse, SectorCreatedResponse, SectorUpdatedResponse, SectorDeletedResponse
from ...infrastructure.container import container
from ...application.use_cases import (
    CreateSectorUseCase, GetSectorUseCase, ListSectorsUseCase,
    UpdateSectorUseCase, DeleteSectorUseCase
)
from ..middleware import auth_middleware

router = APIRouter(tags=["Sectors"])


def get_create_sector_use_case() -> CreateSectorUseCase:
    return CreateSectorUseCase(
        sector_repository=container.sector_repository(),
        sector_type_repository=container.sector_type_repository()
    )


def get_get_sector_use_case() -> GetSectorUseCase:
    return GetSectorUseCase(
        sector_repository=container.sector_repository(),
        sector_type_repository=container.sector_type_repository()
    )


def get_list_sectors_use_case() -> ListSectorsUseCase:
    return ListSectorsUseCase(
        sector_repository=container.sector_repository(),
        sector_type_repository=container.sector_type_repository()
    )


def get_update_sector_use_case() -> UpdateSectorUseCase:
    return UpdateSectorUseCase(
        sector_repository=container.sector_repository(),
        sector_type_repository=container.sector_type_repository()
    )


def get_delete_sector_use_case() -> DeleteSectorUseCase:
    return DeleteSectorUseCase(
        sector_repository=container.sector_repository()
    )


@router.get("/", response_model=SectorListResponse)
async def get_sectors(
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    branch_id: Optional[int] = Query(None, description="Filtrar por sucursal"),
    sector_type_id: Optional[int] = Query(None, description="Filtrar por tipo de sector"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    use_case: ListSectorsUseCase = Depends(get_list_sectors_use_case)
):
    """Listar sectores con filtros"""
    filter_request = SectorFilterRequest(
        name=name,
        branch_id=branch_id,
        sector_type_id=sector_type_id,
        is_active=is_active,
        limit=limit,
        offset=offset
    )
    return await use_case.execute(filter_request)


@router.get("/{sector_id}", response_model=SectorResponse)
async def get_sector(
    sector_id: int,
    use_case: GetSectorUseCase = Depends(get_get_sector_use_case)
):
    """Obtener un sector por ID"""
    sector = await use_case.execute(sector_id)
    if not sector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sector no encontrado"
        )
    return sector


@router.post("/", response_model=SectorCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_sector(
    request: CreateSectorRequest,
    use_case: CreateSectorUseCase = Depends(get_create_sector_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Crear un nuevo sector"""
    return await use_case.execute(request)


@router.put("/{sector_id}", response_model=SectorUpdatedResponse)
async def update_sector(
    sector_id: int,
    request: UpdateSectorRequest,
    use_case: UpdateSectorUseCase = Depends(get_update_sector_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Actualizar un sector"""
    return await use_case.execute(sector_id, request)


@router.delete("/{sector_id}", response_model=SectorDeletedResponse)
async def delete_sector(
    sector_id: int,
    use_case: DeleteSectorUseCase = Depends(get_delete_sector_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    """Eliminar un sector"""
    return await use_case.execute(sector_id)
