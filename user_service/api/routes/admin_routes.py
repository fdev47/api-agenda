"""
Rutas de administración
"""
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
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
    assign_role_use_case = container.assign_role_use_case()
    await assign_role_use_case.execute(user_id, role)
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
    assign_permission_use_case = container.assign_permission_use_case()
    await assign_permission_use_case.execute(user_id, permission)
    return PermissionAssignmentResponse(
        success=True,
        message=f"Permiso '{permission}' asignado al usuario {user_id}",
        user_id=user_id,
        permission=permission
    )


@router.get("/users/{user_id}/roles", response_model=UserRolesResponse)
async def get_user_roles(
    user_id: UUID,
    current_user=Depends(auth_middleware["require_role"]("admin"))
):
    """Obtener roles de un usuario (solo admin)"""
    get_user_roles_use_case = container.get_user_roles_use_case()
    roles = await get_user_roles_use_case.execute(user_id)
    return UserRolesResponse(
        user_id=str(user_id),
        roles=roles
    )


@router.post("/users/{user_id}/activate", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def activate_user(
    user_id: UUID,
    current_user=Depends(auth_middleware["require_role"]("admin"))
):
    """Activar usuario (solo admin)"""
    activate_user_use_case = container.activate_user_use_case()
    user = await activate_user_use_case.execute(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return SuccessResponse(
        success=True,
        message=f"Usuario {user_id} activado exitosamente"
    )


@router.post("/users/{user_id}/deactivate", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def deactivate_user(
    user_id: UUID,
    current_user=Depends(auth_middleware["require_role"]("admin"))
):
    """Desactivar usuario (solo admin)"""
    deactivate_user_use_case = container.deactivate_user_use_case()
    user = await deactivate_user_use_case.execute(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return SuccessResponse(
        success=True,
        message=f"Usuario {user_id} desactivado exitosamente"
    )


@router.delete("/users/{user_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def delete_user_admin(
    user_id: UUID,
    current_user=Depends(auth_middleware["require_role"]("admin"))
):
    """Eliminar usuario (solo admin)"""
    delete_user_use_case = container.delete_user_use_case()
    success = await delete_user_use_case.execute(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return SuccessResponse(
        success=True,
        message=f"Usuario {user_id} eliminado exitosamente"
    ) 