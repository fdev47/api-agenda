"""
Caso de uso para listar tipos de sector
"""
from ...domain.interfaces.sector_type_repository import SectorTypeRepository
from ...domain.dto.requests.sector_type_requests import SectorTypeFilterRequest
from ...domain.dto.responses.sector_type_responses import SectorTypeListResponse, SectorTypeResponse


class ListSectorTypesUseCase:
    """Caso de uso para listar tipos de sector"""
    
    def __init__(self, sector_type_repository: SectorTypeRepository):
        self.sector_type_repository = sector_type_repository
    
    async def execute(self, filter_request: SectorTypeFilterRequest) -> SectorTypeListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener tipos de sector del repositorio
        sector_types, total = await self.sector_type_repository.list(filter_request)
        
        # Convertir a DTOs de respuesta
        sector_type_responses = [
            SectorTypeResponse(
                id=sector_type.id,
                name=sector_type.name,
                code=sector_type.code,
                description=sector_type.description,
                measurement_unit=sector_type.measurement_unit.value,
                merchandise_type=sector_type.merchandise_type,
                is_active=sector_type.is_active,
                created_at=sector_type.created_at,
                updated_at=sector_type.updated_at
            )
            for sector_type in sector_types
        ]
        
        # Calcular página
        page = (filter_request.offset // filter_request.limit) + 1
        
        # Retornar respuesta
        return SectorTypeListResponse(
            sector_types=sector_type_responses,
            total=total,
            page=page,
            size=filter_request.limit
        ) 