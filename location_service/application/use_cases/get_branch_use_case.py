"""
Caso de uso para obtener una sucursal por ID
"""
from ...domain.interfaces.branch_repository import BranchRepository
from ...domain.dto.responses.branch_responses import BranchResponse
from ...domain.exceptions.branch_exceptions import BranchNotFoundException


class GetBranchUseCase:
    """Caso de uso para obtener una sucursal por ID"""
    
    def __init__(self, branch_repository: BranchRepository):
        self.branch_repository = branch_repository
    
    async def execute(self, branch_id: int) -> BranchResponse:
        """Ejecutar el caso de uso"""
        # Obtener la sucursal con todas sus relaciones
        branch_data = await self.branch_repository.get_branch_with_relations(branch_id)
        
        if not branch_data:
            raise BranchNotFoundException(
                f"No se encontró la sucursal con ID {branch_id}",
                entity_id=branch_id
            )
        
        return BranchResponse(**branch_data) 