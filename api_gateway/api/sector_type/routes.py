"""
Rutas de sector types en el API Gateway
"""
from fastapi import APIRouter, Query
from typing import List, Optional
from ...domain.sector_type.dto.responses.sector_type_responses import SectorTypeListResponse
from ...application.sector_type.use_cases.list_sector_types_use_case import ListSectorTypesUseCase

router = APIRouter()


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
        sector_types=sector_types,
        total=len(sector_types),
        page=1,  # Por defecto página 1
        size=limit
    ) 