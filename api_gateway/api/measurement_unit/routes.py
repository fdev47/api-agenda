"""
Rutas de measurement units en el API Gateway
"""
from fastapi import APIRouter, Query
from typing import List, Optional
from ...domain.measurement_unit.dto.responses.measurement_unit_responses import MeasurementUnitListResponse
from ...application.measurement_unit.use_cases.list_measurement_units_use_case import ListMeasurementUnitsUseCase

router = APIRouter()


@router.get("/", response_model=MeasurementUnitListResponse)
async def list_measurement_units(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo")
):
    """
    Listar unidades de medida disponibles
    """
    use_case = ListMeasurementUnitsUseCase()
    measurement_units = await use_case.execute(skip=skip, limit=limit, name=name, code=code, is_active=is_active)
    
    return MeasurementUnitListResponse(
        items=measurement_units,
        total=len(measurement_units),
        limit=limit,
        offset=skip
    ) 