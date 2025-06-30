"""
Rutas de administración
"""
from fastapi import APIRouter, Depends, status
from ...infrastructure.container import container
from ...domain.dto.responses import (
    SuccessResponse, RoleAssignmentResponse, PermissionAssignmentResponse, 
    UserRolesResponse
)
from ..middleware import auth_middleware

router = APIRouter()


@router.post("/users/assign-role", response_model=RoleAssignmentResponse, status_code=status.HTTP_200_OK)
async def assign_role(
    user_id: str,
    role: str,
    current_user=Depends(auth_middleware["require_role"]("admin"))
):
    """Asignar rol a un usuario (solo admin)"""
    await container.assign_role_use_case.execute(user_id, role)
    return RoleAssignmentResponse(
        success=True,
        message=f"Rol '{role}' asignado al usuario {user_id}",
        user_id=user_id,
        role=role
    )


@router.post("/users/assign-permission", response_model=PermissionAssignmentResponse, status_code=status.HTTP_200_OK)
async def assign_permission(
    user_id: str,
    permission: str,
    current_user=Depends(auth_middleware["require_role"]("admin"))
):
    """Asignar permiso a un usuario (solo admin)"""
    await container.assign_permission_use_case.execute(user_id, permission)
    return PermissionAssignmentResponse(
        success=True,
        message=f"Permiso '{permission}' asignado al usuario {user_id}",
        user_id=user_id,
        permission=permission
    )


@router.get("/users/{user_id}/roles", response_model=UserRolesResponse)
async def get_user_roles(
    user_id: str,
    current_user=Depends(auth_middleware["require_role"]("admin"))
):
    """Obtener roles de un usuario (solo admin)"""
    roles = await container.get_user_roles_use_case.execute(user_id)
    return UserRolesResponse(
        user_id=user_id,
        roles=roles
    )


@router.post("/users/{user_id}/activate", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def activate_user(
    user_id: str,
    current_user=Depends(auth_middleware["require_role"]("admin"))
):
    """Activar usuario (solo admin)"""
    await container.activate_user_use_case.execute(user_id)
    return SuccessResponse(
        success=True,
        message=f"Usuario {user_id} activado exitosamente"
    )


@router.post("/users/{user_id}/deactivate", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def deactivate_user(
    user_id: str,
    current_user=Depends(auth_middleware["require_role"]("admin"))
):
    """Desactivar usuario (solo admin)"""
    await container.deactivate_user_use_case.execute(user_id)
    return SuccessResponse(
        success=True,
        message=f"Usuario {user_id} desactivado exitosamente"
    )


@router.delete("/users/{user_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def delete_user_admin(
    user_id: str,
    current_user=Depends(auth_middleware["require_role"]("admin"))
):
    """Eliminar usuario (solo admin)"""
    await container.delete_user_use_case.execute(user_id)
    return SuccessResponse(
        success=True,
        message=f"Usuario {user_id} eliminado exitosamente"
    ) 