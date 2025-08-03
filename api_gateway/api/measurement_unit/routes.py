"""
Rutas de measurement units en el API Gateway
"""
from fastapi import APIRouter, Query, Depends, Header, HTTPException, status
from typing import List, Optional
from ..middleware import auth_middleware
from ...domain.measurement_unit.dto.requests.measurement_unit_requests import CreateMeasurementUnitRequest, UpdateMeasurementUnitRequest
from ...domain.measurement_unit.dto.responses.measurement_unit_responses import (
    MeasurementUnitListResponse, MeasurementUnitResponse, MeasurementUnitCreatedResponse, 
    MeasurementUnitUpdatedResponse, MeasurementUnitDeletedResponse
)
from ...application.measurement_unit.use_cases.list_measurement_units_use_case import ListMeasurementUnitsUseCase
from ...application.measurement_unit.use_cases.create_measurement_unit_use_case import CreateMeasurementUnitUseCase
from ...application.measurement_unit.use_cases.get_measurement_unit_use_case import GetMeasurementUnitUseCase
from ...application.measurement_unit.use_cases.update_measurement_unit_use_case import UpdateMeasurementUnitUseCase
from ...application.measurement_unit.use_cases.delete_measurement_unit_use_case import DeleteMeasurementUnitUseCase

router = APIRouter()


@router.post("/", response_model=MeasurementUnitCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_measurement_unit(
    request: CreateMeasurementUnitRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Crear una nueva unidad de medida (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = CreateMeasurementUnitUseCase()
    result = await use_case.execute(request=request, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la unidad de medida"
        )
    
    return result


@router.get("/{measurement_unit_id}", response_model=MeasurementUnitResponse)
async def get_measurement_unit(
    measurement_unit_id: int,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Obtener una unidad de medida por ID (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = GetMeasurementUnitUseCase()
    measurement_unit = await use_case.execute(measurement_unit_id=measurement_unit_id, access_token=access_token)
    
    if not measurement_unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de medida no encontrada"
        )
    
    return measurement_unit


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


@router.put("/{measurement_unit_id}", response_model=MeasurementUnitUpdatedResponse)
async def update_measurement_unit(
    measurement_unit_id: int,
    request: UpdateMeasurementUnitRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Actualizar una unidad de medida (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = UpdateMeasurementUnitUseCase()
    result = await use_case.execute(measurement_unit_id=measurement_unit_id, request=request, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de medida no encontrada"
        )
    
    return result


@router.delete("/{measurement_unit_id}", response_model=MeasurementUnitDeletedResponse)
async def delete_measurement_unit(
    measurement_unit_id: int,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Eliminar una unidad de medida (requiere autenticación)
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    use_case = DeleteMeasurementUnitUseCase()
    result = await use_case.execute(measurement_unit_id=measurement_unit_id, access_token=access_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de medida no encontrada"
        )
    
    return result 