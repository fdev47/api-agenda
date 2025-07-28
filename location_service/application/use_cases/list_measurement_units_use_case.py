"""
Caso de uso para listar unidades de medida
"""
from typing import List, Tuple
from ...domain.entities.measurement_unit_entity import MeasurementUnit
from ...domain.dto.requests.measurement_unit_requests import MeasurementUnitFilterRequest
from ...domain.dto.responses.measurement_unit_responses import MeasurementUnitListResponse, MeasurementUnitResponse
from ...domain.interfaces.measurement_unit_repository import MeasurementUnitRepository


class ListMeasurementUnitsUseCase:
    """Caso de uso para listar unidades de medida"""
    
    def __init__(self, measurement_unit_repository: MeasurementUnitRepository):
        self.measurement_unit_repository = measurement_unit_repository
    
    async def execute(self, filter_request: MeasurementUnitFilterRequest) -> MeasurementUnitListResponse:
        """Ejecutar el caso de uso"""
        measurement_units, total = await self.measurement_unit_repository.list_all(filter_request)
        
        # Convertir entidades a responses
        items = [
            MeasurementUnitResponse(
                id=mu.id,
                name=mu.name,
                code=mu.code,
                description=mu.description,
                is_active=mu.is_active,
                created_at=mu.created_at,
                updated_at=mu.updated_at
            )
            for mu in measurement_units
        ]
        
        return MeasurementUnitListResponse(
            items=items,
            total=total,
            limit=filter_request.limit,
            offset=filter_request.offset
        ) 