"""
Caso de uso para obtener un local por ID
"""
from ...domain.interfaces.local_repository import LocalRepository
from ...domain.dto.responses.local_responses import LocalResponse
from ...domain.exceptions.local_exceptions import LocalNotFoundException


class GetLocalUseCase:
    """Caso de uso para obtener un local por ID"""
    
    def __init__(self, local_repository: LocalRepository):
        self.local_repository = local_repository
    
    async def execute(self, local_id: int) -> LocalResponse:
        """Ejecutar el caso de uso"""
        # Obtener el local del repositorio
        local = await self.local_repository.get_by_id(local_id)
        
        if not local:
            raise LocalNotFoundException(
                f"No se encontró el local con ID {local_id}",
                entity_id=local_id
            )
        
        return LocalResponse(
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