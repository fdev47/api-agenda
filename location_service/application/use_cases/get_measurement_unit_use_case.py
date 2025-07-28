"""
Caso de uso para obtener una unidad de medida por ID
"""
from typing import Optional
from ...domain.entities.measurement_unit_entity import MeasurementUnit
from ...domain.interfaces.measurement_unit_repository import MeasurementUnitRepository


class GetMeasurementUnitUseCase:
    """Caso de uso para obtener una unidad de medida por ID"""
    
    def __init__(self, measurement_unit_repository: MeasurementUnitRepository):
        self.measurement_unit_repository = measurement_unit_repository
    
    async def execute(self, measurement_unit_id: int) -> Optional[MeasurementUnit]:
        """Ejecutar el caso de uso"""
        return await self.measurement_unit_repository.get_by_id(measurement_unit_id) 