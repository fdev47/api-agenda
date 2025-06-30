"""
Caso de uso para eliminar un local
"""
from ...domain.interfaces.local_repository import LocalRepository
from ...domain.dto.responses.local_responses import LocalDeletedResponse
from ...domain.exceptions.local_exceptions import LocalNotFoundException


class DeleteLocalUseCase:
    """Caso de uso para eliminar un local"""
    
    def __init__(self, local_repository: LocalRepository):
        self.local_repository = local_repository
    
    async def execute(self, local_id: int) -> LocalDeletedResponse:
        """Ejecutar el caso de uso"""
        # Verificar si el local existe
        existing_local = await self.local_repository.get_by_id(local_id)
        if not existing_local:
            raise LocalNotFoundException(
                f"No se encontró el local con ID {local_id}",
                entity_id=local_id
            )
        
        # Eliminar del repositorio
        success = await self.local_repository.delete(local_id)
        
        if not success:
            raise LocalNotFoundException(
                f"No se pudo eliminar el local con ID {local_id}",
                entity_id=local_id
            )
        
        return LocalDeletedResponse(
            id=local_id,
            message="Local eliminado exitosamente"
        ) 