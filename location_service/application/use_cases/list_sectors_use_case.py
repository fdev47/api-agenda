"""
Caso de uso para listar sectores
"""
from typing import List
from ...domain.interfaces.sector_repository import SectorRepository
from ...domain.interfaces.sector_type_repository import SectorTypeRepository
from ...domain.dto.requests.sector_requests import SectorFilterRequest
from ...domain.dto.responses.sector_responses import SectorResponse, SectorListResponse


class ListSectorsUseCase:
    """Caso de uso para listar sectores"""
    
    def __init__(self, sector_repository: SectorRepository, sector_type_repository: SectorTypeRepository):
        self.sector_repository = sector_repository
        self.sector_type_repository = sector_type_repository
    
    async def execute(self, filter_request: SectorFilterRequest) -> SectorListResponse:
        """Ejecutar el caso de uso"""
        
        # Obtener sectores del repositorio
        sectors, total = await self.sector_repository.list(filter_request)
        
        # Convertir a respuestas
        sector_responses = []
        for sector in sectors:
            # Obtener el tipo de sector para la unidad de medida
            sector_type = await self.sector_type_repository.get_by_id(sector.sector_type_id)
            
            sector_responses.append(SectorResponse(
                id=sector.id,
                name=sector.name,
                description=sector.description,
                branch_id=sector.branch_id,
                sector_type_id=sector.sector_type_id,
                measurement_unit=sector_type.measurement_unit.value if sector_type else None,
                is_active=sector.is_active,
                created_at=sector.created_at,
                updated_at=sector.updated_at
            ))
        
        # Calcular página
        page = (filter_request.offset // filter_request.limit) + 1
        
        # Retornar respuesta
        return SectorListResponse(
            sectors=sector_responses,
            total=total,
            page=page,
            size=filter_request.limit
        ) 