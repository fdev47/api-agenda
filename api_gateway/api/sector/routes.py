"""
Rutas de sectores en el API Gateway
"""
from fastapi import APIRouter, Query, Depends, Header, HTTPException, status
from typing import List, Optional
from ..middleware import auth_middleware
from ...domain.sector.dto.requests.sector_requests import CreateSectorRequest, UpdateSectorRequest
from ...domain.sector.dto.responses.sector_responses import (
    SectorListResponse, SectorResponse, SectorCreatedResponse, 
    SectorUpdatedResponse, SectorDeletedResponse
)
from ...application.sector.use_cases.list_sectors_use_case import ListSectorsUseCase
from ...application.sector.use_cases.create_sector_use_case import CreateSectorUseCase
from ...application.sector.use_cases.get_sector_use_case import GetSectorUseCase
from ...application.sector.use_cases.update_sector_use_case import UpdateSectorUseCase
from ...application.sector.use_cases.delete_sector_use_case import DeleteSectorUseCase

router = APIRouter()


@router.post("/", response_model=SectorCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_sector(
    request: CreateSectorRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Crear un nuevo sector (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = CreateSectorUseCase()
    result = await use_case.execute(request=request, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el sector"
        )
    
    return result


@router.get("/{sector_id}", response_model=SectorResponse)
async def get_sector(
    sector_id: int,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Obtener un sector por ID (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = GetSectorUseCase()
    sector = await use_case.execute(sector_id=sector_id, access_token=access_token)
    
    if not sector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sector no encontrado"
        )
    
    return sector


@router.get("/", response_model=SectorListResponse)
async def list_sectors(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    branch_id: Optional[int] = Query(None, description="Filtrar por sucursal"),
    sector_type_id: Optional[int] = Query(None, description="Filtrar por tipo de sector"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Listar sectores disponibles (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = ListSectorsUseCase()
    sectors = await use_case.execute(skip=skip, limit=limit, name=name, branch_id=branch_id, sector_type_id=sector_type_id, is_active=is_active, access_token=access_token)
    
    return SectorListResponse(
        sectors=sectors,
        total=len(sectors),
        limit=limit,
        offset=skip
    )


@router.put("/{sector_id}", response_model=SectorUpdatedResponse)
async def update_sector(
    sector_id: int,
    request: UpdateSectorRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Actualizar un sector (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = UpdateSectorUseCase()
    result = await use_case.execute(sector_id=sector_id, request=request, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sector no encontrado"
        )
    
    return result


@router.delete("/{sector_id}", response_model=SectorDeletedResponse)
async def delete_sector(
    sector_id: int,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Eliminar un sector (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = DeleteSectorUseCase()
    result = await use_case.execute(sector_id=sector_id, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sector no encontrado"
        )
    
    return result
