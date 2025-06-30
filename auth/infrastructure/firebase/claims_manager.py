"""Firebase User Claims Manager implementation"""

from typing import List
from firebase_admin.exceptions import FirebaseError

from ...domain.interfaces import IUserClaimsManager
from ...domain.models import CustomClaims, AuthError, AuthErrorCode


class FirebaseUserClaimsManager(IUserClaimsManager):
    """Gestor de claims específico para Firebase"""
    
    def __init__(self, auth_provider):
        self._auth_provider = auth_provider
    
    def set_user_role(self, user_id: str, role: str) -> None:
        try:
            user = self._auth_provider.get_user_by_id(user_id)
            if not user:
                raise AuthError("Usuario no encontrado", AuthErrorCode.USER_NOT_FOUND.value)
            
            current_claims = user.custom_claims
            roles = current_claims.get('roles', [])
            
            if role not in roles:
                roles.append(role)
                
            claims = CustomClaims(
                roles=roles,
                permissions=current_claims.get('permissions', []),
                organization_id=current_claims.get('organization_id')
            )
            
            self._auth_provider.update_user_claims(user_id, claims)
            
        except FirebaseError as e:
            raise self._auth_provider._map_firebase_error(e)
    
    def add_user_permission(self, user_id: str, permission: str) -> None:
        try:
            user = self._auth_provider.get_user_by_id(user_id)
            if not user:
                raise AuthError("Usuario no encontrado", AuthErrorCode.USER_NOT_FOUND.value)
            
            current_claims = user.custom_claims
            permissions = current_claims.get('permissions', [])
            
            if permission not in permissions:
                permissions.append(permission)
                
            claims = CustomClaims(
                roles=current_claims.get('roles', []),
                permissions=permissions,
                organization_id=current_claims.get('organization_id')
            )
            
            self._auth_provider.update_user_claims(user_id, claims)
            
        except FirebaseError as e:
            raise self._auth_provider._map_firebase_error(e)
    
    def get_user_roles(self, user_id: str) -> List[str]:
        user = self._auth_provider.get_user_by_id(user_id)
        if not user:
            raise AuthError("Usuario no encontrado", AuthErrorCode.USER_NOT_FOUND.value)
        
        return user.custom_claims.get('roles', []) 