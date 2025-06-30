"""
Caso de uso para eliminar una sucursal
"""
from ...domain.interfaces.branch_repository import BranchRepository
from ...domain.dto.responses.branch_responses import BranchDeletedResponse
from ...domain.exceptions.branch_exceptions import BranchNotFoundException


class DeleteBranchUseCase:
    """Caso de uso para eliminar una sucursal"""
    
    def __init__(self, branch_repository: BranchRepository):
        self.branch_repository = branch_repository
    
    async def execute(self, branch_id: int) -> BranchDeletedResponse:
        """Ejecutar el caso de uso"""
        # Verificar si la sucursal existe
        existing_branch = await self.branch_repository.get_by_id(branch_id)
        if not existing_branch:
            raise BranchNotFoundException(
                f"No se encontró la sucursal con ID {branch_id}",
                entity_id=branch_id
            )
        
        # Eliminar del repositorio
        success = await self.branch_repository.delete(branch_id)
        
        if not success:
            raise BranchNotFoundException(
                f"No se pudo eliminar la sucursal con ID {branch_id}",
                entity_id=branch_id
            )
        
        return BranchDeletedResponse(
            id=branch_id,
            message="Sucursal eliminada exitosamente"
        ) 