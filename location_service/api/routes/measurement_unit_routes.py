"""
Rutas para gestión de unidades de medida
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from ...domain.dto.requests import CreateMeasurementUnitRequest, UpdateMeasurementUnitRequest
from ...domain.dto.responses import MeasurementUnitResponse, MeasurementUnitListResponse
from ...infrastructure.container import container
from ...application.use_cases import (
    CreateMeasurementUnitUseCase, GetMeasurementUnitUseCase, ListMeasurementUnitsUseCase,
    UpdateMeasurementUnitUseCase, DeleteMeasurementUnitUseCase
)
from ...domain.dto.requests import MeasurementUnitFilterRequest
from ..middleware import auth_middleware

router = APIRouter(tags=["Measurement Units"])


def get_create_measurement_unit_use_case() -> CreateMeasurementUnitUseCase:
    return CreateMeasurementUnitUseCase(
        measurement_unit_repository=container.measurement_unit_repository()
    )

def get_get_measurement_unit_use_case() -> GetMeasurementUnitUseCase:
    return GetMeasurementUnitUseCase(
        measurement_unit_repository=container.measurement_unit_repository()
    )

def get_list_measurement_units_use_case() -> ListMeasurementUnitsUseCase:
    return ListMeasurementUnitsUseCase(
        measurement_unit_repository=container.measurement_unit_repository()
    )

def get_update_measurement_unit_use_case() -> UpdateMeasurementUnitUseCase:
    return UpdateMeasurementUnitUseCase(
        measurement_unit_repository=container.measurement_unit_repository()
    )

def get_delete_measurement_unit_use_case() -> DeleteMeasurementUnitUseCase:
    return DeleteMeasurementUnitUseCase(
        measurement_unit_repository=container.measurement_unit_repository()
    )


@router.get("/", response_model=MeasurementUnitListResponse)
async def get_measurement_units(
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    code: Optional[str] = Query(None, description="Filtrar por código"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    use_case: ListMeasurementUnitsUseCase = Depends(get_list_measurement_units_use_case)
):
    """Listar unidades de medida con filtros"""
    filter_request = MeasurementUnitFilterRequest(
        name=name,
        code=code,
        is_active=is_active,
        limit=limit,
        offset=offset
    )
    return await use_case.execute(filter_request)


@router.get("/{measurement_unit_id}", response_model=MeasurementUnitResponse)
async def get_measurement_unit(
    measurement_unit_id: int,
    use_case: GetMeasurementUnitUseCase = Depends(get_get_measurement_unit_use_case)
):
    measurement_unit = await use_case.execute(measurement_unit_id)
    if not measurement_unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de medida no encontrada"
        )
    return measurement_unit


@router.post("/", response_model=MeasurementUnitResponse, status_code=status.HTTP_201_CREATED)
async def create_measurement_unit(
    request: CreateMeasurementUnitRequest,
    use_case: CreateMeasurementUnitUseCase = Depends(get_create_measurement_unit_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    return await use_case.execute(request)


@router.put("/{measurement_unit_id}", response_model=MeasurementUnitResponse)
async def update_measurement_unit(
    measurement_unit_id: int,
    request: UpdateMeasurementUnitRequest,
    use_case: UpdateMeasurementUnitUseCase = Depends(get_update_measurement_unit_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    measurement_unit = await use_case.execute(measurement_unit_id, request)
    if not measurement_unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de medida no encontrada"
        )
    return measurement_unit


@router.delete("/{measurement_unit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_measurement_unit(
    measurement_unit_id: int,
    use_case: DeleteMeasurementUnitUseCase = Depends(get_delete_measurement_unit_use_case),
    current_user=Depends(auth_middleware["require_auth"])
):
    success = await use_case.execute(measurement_unit_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de medida no encontrada"
        ) 