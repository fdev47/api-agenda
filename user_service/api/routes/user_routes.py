"""
Rutas de usuarios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from ...domain.dto.requests import CreateUserRequest, UpdateUserRequest
from ...domain.dto.responses import UserResponse, UserListResponse, SuccessResponse
from ...infrastructure.container import container
from ..middleware import auth_middleware

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserRequest):
    """
    Crear un nuevo usuario
    - Crea en Firebase primero
    - Si Firebase es exitoso, crea en PostgreSQL
    - Si Firebase falla, no toca PostgreSQL
    """
    try:
        create_use_case = container.create_user_use_case()
        user = await create_use_case.execute(request)
        return user
    except Exception as e:
        # Si falla, la excepción ya está manejada en el use case
        raise e


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user=Depends(auth_middleware["require_auth"])):
    """Obtener información del usuario actual"""
    auth_uid = current_user["user_id"]
    get_use_case = container.get_user_by_auth_uid_use_case()
    user = await get_use_case.execute(auth_uid)
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: UUID, current_user=Depends(auth_middleware["require_auth"])):
    """Obtener usuario por ID (requiere autenticación)"""
    get_use_case = container.get_user_by_id_use_case()
    user = await get_use_case.execute(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user


@router.get("/", response_model=UserListResponse)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(auth_middleware["require_auth"])
):
    """Listar usuarios (requiere autenticación)"""
    list_use_case = container.list_users_use_case()
    users = await list_use_case.execute(skip=skip, limit=limit)
    return users


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    current_user=Depends(auth_middleware["require_auth"])
):
    """Actualizar usuario (requiere autenticación)"""
    update_use_case = container.update_user_use_case()
    user = await update_use_case.execute(user_id, request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user


@router.delete("/{user_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: UUID,
    current_user=Depends(auth_middleware["require_auth"])
):
    """Eliminar usuario (requiere autenticación)"""
    delete_use_case = container.delete_user_use_case()
    success = await delete_use_case.execute(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return SuccessResponse(
        success=True,
        message=f"Usuario {user_id} eliminado exitosamente"
    ) 