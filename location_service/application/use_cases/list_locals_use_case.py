"""
Caso de uso para listar locales
"""
from ...domain.interfaces.local_repository import LocalRepository
from ...domain.dto.requests.local_requests import LocalFilterRequest
from ...domain.dto.responses.local_responses import LocalListResponse, LocalResponse


class ListLocalsUseCase:
    """Caso de uso para listar locales"""
    
    def __init__(self, local_repository: LocalRepository):
        self.local_repository = local_repository
    
    async def execute(self, filter_request: LocalFilterRequest) -> LocalListResponse:
        """Ejecutar el caso de uso"""
        # Obtener locales del repositorio
        locals, total = await self.local_repository.list_all(filter_request)
        
        # Convertir a responses
        local_responses = [
            LocalResponse(
                id=local.id,
                name=local.name,
                code=local.code,
                description=local.description,
                phone=local.phone,
                email=local.email,
                is_active=local.is_active,
                created_at=local.created_at,
                updated_at=local.updated_at
            )
            for local in locals
        ]
        
        return LocalListResponse(
            locals=local_responses,
            total=total,
            limit=filter_request.limit,
            offset=filter_request.offset
        ) 