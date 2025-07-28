"""
Caso de uso para actualizar una unidad de medida
"""
from typing import Optional
from ...domain.entities.measurement_unit_entity import MeasurementUnit
from ...domain.dto.requests.measurement_unit_requests import UpdateMeasurementUnitRequest
from ...domain.interfaces.measurement_unit_repository import MeasurementUnitRepository


class UpdateMeasurementUnitUseCase:
    """Caso de uso para actualizar una unidad de medida"""
    
    def __init__(self, measurement_unit_repository: MeasurementUnitRepository):
        self.measurement_unit_repository = measurement_unit_repository
    
    async def execute(self, measurement_unit_id: int, request: UpdateMeasurementUnitRequest) -> Optional[MeasurementUnit]:
        """Ejecutar el caso de uso"""
        # Obtener la unidad de medida existente
        existing_measurement_unit = await self.measurement_unit_repository.get_by_id(measurement_unit_id)
        if not existing_measurement_unit:
            return None
        
        # Actualizar campos
        if request.name is not None:
            existing_measurement_unit.name = request.name
        if request.code is not None:
            existing_measurement_unit.code = request.code
        if request.description is not None:
            existing_measurement_unit.description = request.description
        if request.is_active is not None:
            existing_measurement_unit.is_active = request.is_active
        
        # Guardar en el repositorio
        updated_measurement_unit = await self.measurement_unit_repository.update(measurement_unit_id, existing_measurement_unit)
        
        return updated_measurement_unit 