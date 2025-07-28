"""
Caso de uso para eliminar una unidad de medida
"""
from ...domain.interfaces.measurement_unit_repository import MeasurementUnitRepository


class DeleteMeasurementUnitUseCase:
    """Caso de uso para eliminar una unidad de medida"""
    
    def __init__(self, measurement_unit_repository: MeasurementUnitRepository):
        self.measurement_unit_repository = measurement_unit_repository
    
    async def execute(self, measurement_unit_id: int) -> bool:
        """Ejecutar el caso de uso"""
        return await self.measurement_unit_repository.delete(measurement_unit_id) 