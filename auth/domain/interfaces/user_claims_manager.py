"""
Interfaz IUserClaimsManager del dominio
"""
from abc import ABC, abstractmethod
from typing import List


class IUserClaimsManager(ABC):
    """Interface para manejo de claims de usuario"""
    
    @abstractmethod
    def set_user_role(self, user_id: str, role: str) -> None:
        """Establecer un rol para un usuario"""
        pass
    
    @abstractmethod
    def add_user_permission(self, user_id: str, permission: str) -> None:
        """Agregar un permiso a un usuario"""
        pass
    
    @abstractmethod
    def get_user_roles(self, user_id: str) -> List[str]:
        """Obtener los roles de un usuario"""
        pass 