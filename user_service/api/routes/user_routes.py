"""
Rutas de usuarios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
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
        user = await container.create_user_use_case.execute(request)
        return user
    except Exception as e:
        # Si falla, la excepción ya está manejada en el use case
        raise e


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user=Depends(auth_middleware["require_auth"])):
    """Obtener información del usuario actual"""
    user_id = current_user["user_id"]
    user = await container.get_user_by_id_use_case.execute(user_id)
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str, current_user=Depends(auth_middleware["require_auth"])):
    """Obtener usuario por ID (requiere autenticación)"""
    user = await container.get_user_by_id_use_case.execute(user_id)
    return user


@router.get("/", response_model=UserListResponse)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(auth_middleware["require_auth"])
):
    """Listar usuarios (requiere autenticación)"""
    users = await container.list_users_use_case.execute(skip=skip, limit=limit)
    return users


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    request: UpdateUserRequest,
    current_user=Depends(auth_middleware["require_auth"])
):
    """Actualizar usuario (requiere autenticación)"""
    user = await container.update_user_use_case.execute(user_id, request)
    return user


@router.delete("/{user_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: str,
    current_user=Depends(auth_middleware["require_auth"])
):
    """Eliminar usuario (requiere autenticación)"""
    await container.delete_user_use_case.execute(user_id)
    return SuccessResponse(
        success=True,
        message=f"Usuario {user_id} eliminado exitosamente"
    ) 