"""
Use case para eliminar usuarios usando auth_service y user_service
"""
from uuid import UUID
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_internal_error, raise_not_found_error
from ..utils.error_handler import handle_auth_service_error

class DeleteUserUseCase:
    """Use case para eliminar usuarios usando auth_service y user_service"""
    
    def __init__(self):
        self.auth_service_url = config.AUTH_SERVICE_URL
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, user_id: UUID, access_token: str = None) -> bool:
        """
        Eliminar usuario de Firebase y de la base de datos
        
        Args:
            user_id: ID del usuario a eliminar
            access_token: Token de acceso para las llamadas a los servicios
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            # 1. Obtener información del usuario para obtener el auth_uid
            user_info = await self._get_user_info(user_id, access_token)
            auth_uid = user_info["auth_uid"]
            
            # 2. Eliminar usuario de Firebase (auth_service)
            await self._delete_firebase_user(auth_uid, access_token)
            
            # 3. Eliminar usuario de la base de datos (user_service)
            await self._delete_db_user(user_id, access_token)
            
            return True
            
        except Exception as e:
            handle_auth_service_error(e)
    
    async def _get_user_info(self, user_id: UUID, access_token: str) -> dict:
        """Obtener información del usuario para obtener el auth_uid"""
        async with APIClient(self.user_service_url, access_token) as client:
                response = await client.get(f"{config.API_PREFIX}/users/{user_id}")
                return response
    
    async def _delete_firebase_user(self, auth_uid: str, access_token: str):
        """Eliminar usuario de Firebase"""
        async with APIClient(self.auth_service_url, access_token) as client:
                await client.delete(f"{config.API_PREFIX}/auth/users/{auth_uid}")
    
    async def _delete_db_user(self, user_id: UUID, access_token: str):
        """Eliminar usuario de la base de datos"""
        async with APIClient(self.user_service_url, access_token) as client:
                await client.delete(f"{config.API_PREFIX}/users/{user_id}")
