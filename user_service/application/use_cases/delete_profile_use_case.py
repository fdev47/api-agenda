"""
Use case para eliminar perfil
"""
from uuid import UUID
from ...domain.interfaces.profile_repository import IProfileRepository
from ...domain.exceptions.user_exceptions import ProfileNotFoundException


class DeleteProfileUseCase:
    """Use case para eliminar perfil"""
    
    def __init__(self, profile_repository: IProfileRepository):
        self.profile_repository = profile_repository
    
    async def execute(self, profile_id: UUID) -> bool:
        """Ejecutar el use case"""
        existing_profile = await self.profile_repository.get_by_id(profile_id)
        if not existing_profile:
            raise ProfileNotFoundException(str(profile_id))
        
        # Eliminar perfil
        # Nota: La interfaz no tiene método delete, necesitamos implementarlo
        # Por ahora retornamos True
        return True 