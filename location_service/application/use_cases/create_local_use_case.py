"""
Caso de uso para crear un local
"""
from ...domain.interfaces.local_repository import LocalRepository
from ...domain.entities.local import Local
from ...domain.dto.requests.local_requests import CreateLocalRequest
from ...domain.dto.responses.local_responses import LocalCreatedResponse
from ...domain.exceptions.local_exceptions import LocalAlreadyExistsException


class CreateLocalUseCase:
    """Caso de uso para crear un local"""
    
    def __init__(self, local_repository: LocalRepository):
        self.local_repository = local_repository
    
    async def execute(self, request: CreateLocalRequest) -> LocalCreatedResponse:
        """Ejecutar el caso de uso"""
        # Verificar si ya existe un local con el mismo código
        if await self.local_repository.exists_by_code(request.code):
            raise LocalAlreadyExistsException(
                f"Ya existe un local con el código '{request.code}'",
                code=request.code
            )
        
        # Crear la entidad local
        local = Local(
            name=request.name,
            code=request.code,
            description=request.description,
            phone=request.phone,
            email=request.email,
            is_active=request.is_active
        )
        
        # Guardar en el repositorio
        created_local = await self.local_repository.create(local)
        
        return LocalCreatedResponse(
            id=created_local.id,
            message="Local creado exitosamente"
        ) 