"""
Rutas de roles
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.dto.requests import CreateRoleRequest, UpdateRoleRequest
from ...domain.dto.responses import RoleResponse, RoleListResponse, SuccessResponse
from ...infrastructure.container import container
from ...infrastructure.connection import get_db_session
from ..middleware import auth_middleware
from commons.error_utils import raise_not_found_error, raise_internal_error
from commons.error_codes import ErrorCode

router = APIRouter()


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    request: CreateRoleRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Crear un nuevo rol"""
    try:
        container.db_session.override(db)
        create_use_case = container.create_role_use_case()
        role = await create_use_case.execute(request)
        return role
    except Exception as e:
        raise_internal_error(
            message=f"Error creando rol: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role_by_id(
    role_id: UUID,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Obtener rol por ID"""
    try:
        container.db_session.override(db)
        get_use_case = container.get_role_by_id_use_case()
        role = await get_use_case.execute(role_id)
        return role
    except Exception as e:
        if "RoleNotFoundException" in str(e):
            raise_not_found_error(
                message="Rol no encontrado",
                error_code=ErrorCode.ROLE_NOT_FOUND.value
            )
        raise_internal_error(
            message=f"Error obteniendo rol: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.get("/", response_model=RoleListResponse)
async def list_roles(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Listar roles"""
    try:
        container.db_session.override(db)
        list_use_case = container.list_roles_use_case()
        roles = await list_use_case.execute(skip=skip, limit=limit)
        return RoleListResponse(
            roles=roles,
            total=len(roles),
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise_internal_error(
            message=f"Error listando roles: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: UUID,
    request: UpdateRoleRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Actualizar rol"""
    try:
        container.db_session.override(db)
        update_use_case = container.update_role_use_case()
        role = await update_use_case.execute(role_id, request)
        return role
    except Exception as e:
        if "RoleNotFoundException" in str(e):
            raise_not_found_error(
                message="Rol no encontrado",
                error_code=ErrorCode.ROLE_NOT_FOUND.value
            )
        raise_internal_error(
            message=f"Error actualizando rol: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.delete("/{role_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def delete_role(
    role_id: UUID,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Eliminar rol"""
    try:
        container.db_session.override(db)
        delete_use_case = container.delete_role_use_case()
        success = await delete_use_case.execute(role_id)
        return SuccessResponse(
            success=True,
            message=f"Rol {role_id} eliminado exitosamente"
        )
    except Exception as e:
        if "RoleNotFoundException" in str(e):
            raise_not_found_error(
                message="Rol no encontrado",
                error_code=ErrorCode.ROLE_NOT_FOUND.value
            )
        raise_internal_error(
            message=f"Error eliminando rol: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        ) 