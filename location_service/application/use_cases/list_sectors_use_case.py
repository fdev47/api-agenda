"""
Caso de uso para listar sectores
"""
from typing import List
from ...domain.interfaces.sector_repository import SectorRepository
from ...domain.dto.requests.sector_requests import SectorFilterRequest
from ...domain.dto.responses.sector_responses import SectorResponse, SectorListResponse


class ListSectorsUseCase:
    """Caso de uso para listar sectores"""
    
    def __init__(self, sector_repository: SectorRepository):
        self.sector_repository = sector_repository
    
    async def execute(self, filter_request: SectorFilterRequest) -> SectorListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener sectores del repositorio
        sectors, total = await self.sector_repository.list(filter_request)
        
        # Convertir a respuestas
        sector_responses = [
            SectorResponse(
                id=sector.id,
                name=sector.name,
                description=sector.description,
                branch_id=sector.branch_id,
                sector_type_id=sector.sector_type_id,
                measurement_unit=sector.measurement_unit.value,
                created_at=sector.created_at,
                updated_at=sector.updated_at
            )
            for sector in sectors
        ]
        
        # Retornar respuesta
        return SectorListResponse(
            items=sector_responses,
            total=total,
            page=filter_request.page,
            size=filter_request.limit,
            pages=(total + filter_request.limit - 1) // filter_request.limit
        ) 