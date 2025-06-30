"""
Caso de uso para actualizar un local
"""
from ...domain.interfaces.local_repository import LocalRepository
from ...domain.entities.local import Local
from ...domain.dto.requests.local_requests import UpdateLocalRequest
from ...domain.dto.responses.local_responses import LocalUpdatedResponse
from ...domain.exceptions.local_exceptions import LocalNotFoundException, LocalAlreadyExistsException


class UpdateLocalUseCase:
    """Caso de uso para actualizar un local"""
    
    def __init__(self, local_repository: LocalRepository):
        self.local_repository = local_repository
    
    async def execute(self, local_id: int, request: UpdateLocalRequest) -> LocalUpdatedResponse:
        """Ejecutar el caso de uso"""
        # Verificar si el local existe
        existing_local = await self.local_repository.get_by_id(local_id)
        if not existing_local:
            raise LocalNotFoundException(
                f"No se encontró el local con ID {local_id}",
                entity_id=local_id
            )
        
        # Verificar si el código ya existe (si se está actualizando)
        if request.code and request.code != existing_local.code:
            if await self.local_repository.exists_by_code(request.code, exclude_id=local_id):
                raise LocalAlreadyExistsException(
                    f"Ya existe un local con el código '{request.code}'",
                    code=request.code
                )
        
        # Crear la entidad local con los datos actualizados
        updated_local = Local(
            id=local_id,
            name=request.name if request.name is not None else existing_local.name,
            code=request.code if request.code is not None else existing_local.code,
            description=request.description if request.description is not None else existing_local.description,
            phone=request.phone if request.phone is not None else existing_local.phone,
            email=request.email if request.email is not None else existing_local.email,
            is_active=request.is_active if request.is_active is not None else existing_local.is_active,
            created_at=existing_local.created_at,
            updated_at=existing_local.updated_at
        )
        
        # Actualizar en el repositorio
        await self.local_repository.update(local_id, updated_local)
        
        return LocalUpdatedResponse(
            id=local_id,
            message="Local actualizado exitosamente"
        ) 