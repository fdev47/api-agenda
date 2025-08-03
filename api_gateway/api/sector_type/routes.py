"""
Rutas de sector types en el API Gateway
"""
from fastapi import APIRouter, Query, Depends, Header, HTTPException, status
from typing import List, Optional
from ..middleware import auth_middleware
from ...domain.sector_type.dto.requests.sector_type_requests import CreateSectorTypeRequest, UpdateSectorTypeRequest
from ...domain.sector_type.dto.responses.sector_type_responses import (
    SectorTypeListResponse, SectorTypeResponse, SectorTypeCreatedResponse, 
    SectorTypeUpdatedResponse, SectorTypeDeletedResponse
)
from ...application.sector_type.use_cases.list_sector_types_use_case import ListSectorTypesUseCase
from ...application.sector_type.use_cases.create_sector_type_use_case import CreateSectorTypeUseCase
from ...application.sector_type.use_cases.get_sector_type_use_case import GetSectorTypeUseCase
from ...application.sector_type.use_cases.update_sector_type_use_case import UpdateSectorTypeUseCase
from ...application.sector_type.use_cases.delete_sector_type_use_case import DeleteSectorTypeUseCase

router = APIRouter()


@router.post("/", response_model=SectorTypeCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_sector_type(
    request: CreateSectorTypeRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Crear un nuevo tipo de sector (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = CreateSectorTypeUseCase()
    result = await use_case.execute(request=request, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el tipo de sector"
        )
    
    return result


@router.get("/{sector_type_id}", response_model=SectorTypeResponse)
async def get_sector_type(
    sector_type_id: int,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Obtener un tipo de sector por ID (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = GetSectorTypeUseCase()
    sector_type = await use_case.execute(sector_type_id=sector_type_id, access_token=access_token)
    
    if not sector_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de sector no encontrado"
        )
    
    return sector_type


@router.get("/", response_model=SectorTypeListResponse)
async def list_sector_types(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo")
):
    """
    Listar tipos de sector disponibles
    """
    use_case = ListSectorTypesUseCase()
    sector_types = await use_case.execute(skip=skip, limit=limit, name=name, code=code, is_active=is_active)
    
    return SectorTypeListResponse(
        items=sector_types,
        total=len(sector_types),
        limit=limit,
        offset=skip
    )


@router.put("/{sector_type_id}", response_model=SectorTypeUpdatedResponse)
async def update_sector_type(
    sector_type_id: int,
    request: UpdateSectorTypeRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Actualizar un tipo de sector (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = UpdateSectorTypeUseCase()
    result = await use_case.execute(sector_type_id=sector_type_id, request=request, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de sector no encontrado"
        )
    
    return result


@router.delete("/{sector_type_id}", response_model=SectorTypeDeletedResponse)
async def delete_sector_type(
    sector_type_id: int,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Eliminar un tipo de sector (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = DeleteSectorTypeUseCase()
    result = await use_case.execute(sector_type_id=sector_type_id, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de sector no encontrado"
        )
    
    return result 