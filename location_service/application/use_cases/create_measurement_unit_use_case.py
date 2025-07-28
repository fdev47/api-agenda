"""
Caso de uso para crear una unidad de medida
"""
from ...domain.entities.measurement_unit_entity import MeasurementUnit
from ...domain.dto.requests.measurement_unit_requests import CreateMeasurementUnitRequest
from ...domain.interfaces.measurement_unit_repository import MeasurementUnitRepository


class CreateMeasurementUnitUseCase:
    """Caso de uso para crear una unidad de medida"""
    
    def __init__(self, measurement_unit_repository: MeasurementUnitRepository):
        self.measurement_unit_repository = measurement_unit_repository
    
    async def execute(self, request: CreateMeasurementUnitRequest) -> MeasurementUnit:
        """Ejecutar el caso de uso"""
        # Crear entidad del dominio
        measurement_unit = MeasurementUnit(
            id=0,  # Se asignará automáticamente
            name=request.name,
            code=request.code,
            description=request.description,
            is_active=request.is_active,
            created_at=None,  # Se asignará automáticamente
            updated_at=None
        )
        
        # Guardar en el repositorio
        created_measurement_unit = await self.measurement_unit_repository.create(measurement_unit)
        
        return created_measurement_unit 