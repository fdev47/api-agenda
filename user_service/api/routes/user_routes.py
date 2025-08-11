"""
Rutas de usuarios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.dto.requests import CreateUserRequest, UpdateUserRequest
from ...domain.dto.responses import UserResponse, UserListResponse, SuccessResponse
from ...infrastructure.container import container
from ...infrastructure.connection import get_db_session
from ..middleware import auth_middleware
from ...domain.exceptions.user_exceptions import UserNotFoundException
from commons.error_utils import raise_not_found_error, raise_internal_error
from commons.error_codes import ErrorCode

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Crear un nuevo usuario
    - Crea en Firebase primero
    - Si Firebase es exitoso, crea en PostgreSQL
    - Si Firebase falla, no toca PostgreSQL
    """
    try:
        # Inyectar la sesión de base de datos en el contenedor
        container.db_session.override(db)
        create_use_case = container.create_user_use_case()
        user = await create_use_case.execute(request)
        return user
    except Exception as e:
        # Si falla, la excepción ya está manejada en el use case
        raise e


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Obtener información del usuario actual"""
    try:
        auth_uid = current_user["user_id"]
        # Inyectar la sesión de base de datos en el contenedor
        container.db_session.override(db)
        get_use_case = container.get_user_by_auth_uid_use_case()
        user = await get_use_case.execute(auth_uid)
        return user
    except UserNotFoundException as e:
        raise_not_found_error(
            message="Usuario no encontrado en el sistema",
            error_code=ErrorCode.USER_NOT_FOUND.value
        )
    except Exception as e:
        raise_internal_error(
            message=f"Error obteniendo usuario: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: UUID, 
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Obtener usuario por ID (requiere autenticación)"""
    # Inyectar la sesión de base de datos en el contenedor
    container.db_session.override(db)
    get_use_case = container.get_user_by_id_use_case()
    user = await get_use_case.execute(user_id)
    if not user:
        raise_not_found_error(
            message="Usuario no encontrado",
            error_code=ErrorCode.USER_NOT_FOUND.value
        )
    return user


@router.get("/by-username/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Obtener usuario por username (requiere autenticación)"""
    # Inyectar la sesión de base de datos en el contenedor
    container.db_session.override(db)
    get_use_case = container.get_user_by_username_use_case()
    user = await get_use_case.execute(username)
    if not user:
        raise_not_found_error(
            message="Usuario no encontrado",
            error_code=ErrorCode.USER_NOT_FOUND.value
        )
    return user


@router.get("/", response_model=UserListResponse)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Listar usuarios (requiere autenticación)"""
    # Inyectar la sesión de base de datos en el contenedor
    container.db_session.override(db)
    list_use_case = container.list_users_use_case()
    users = await list_use_case.execute(skip=skip, limit=limit)
    return users


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Actualizar usuario (requiere autenticación)"""
    # Inyectar la sesión de base de datos en el contenedor
    container.db_session.override(db)
    update_use_case = container.update_user_use_case()
    user = await update_use_case.execute(user_id, request)
    if not user:
        raise_not_found_error(
            message="Usuario no encontrado",
            error_code=ErrorCode.USER_NOT_FOUND.value
        )
    return user


@router.delete("/{user_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: UUID,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Eliminar usuario (requiere autenticación)"""
    # Inyectar la sesión de base de datos en el contenedor
    container.db_session.override(db)
    delete_use_case = container.delete_user_use_case()
    success = await delete_use_case.execute(user_id)
    if not success:
        raise_not_found_error(
            message="Usuario no encontrado",
            error_code=ErrorCode.USER_NOT_FOUND.value
        )
    return SuccessResponse(
        success=True,
        message=f"Usuario {user_id} eliminado exitosamente"
    ) 