"""
Rutas de usuarios para API Gateway
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from typing import Optional
from uuid import UUID
from ...infrastructure.container import Container
from ..middleware import auth_middleware
from ...domain.user.dto.responses.user_responses import UserResponse, UserListResponse, DeleteUserResponse
from ...domain.user.dto.requests.user_requests import CreateUserRequest, UpdateUserRequest

router = APIRouter()


def get_container() -> Container:
    """Obtener el container de dependencias"""
    return Container()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Crear nuevo usuario (requiere autenticación)"""
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Crear usuario usando el use case
    create_user_use_case = container.create_user_use_case()
    user = await create_user_use_case.execute(request, access_token)
    
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Obtener información del usuario actual"""
    auth_uid = current_user["user_id"]
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Obtener usuario usando el use case
    get_user_use_case = container.get_user_use_case()
    user = await get_user_use_case.execute(auth_uid, access_token)
    
    return user


@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(100, ge=1, le=1000, description="Número de registros por página"),
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Listar usuarios (requiere autenticación)"""
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Obtener lista de usuarios usando el use case
    list_users_use_case = container.list_users_use_case()
    users = await list_users_use_case.execute(page=page, size=size, access_token=access_token)
    
    return users


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Actualizar usuario (requiere autenticación)"""
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Actualizar usuario usando el use case
    update_user_use_case = container.update_user_use_case()
    user = await update_user_use_case.execute(user_id, request, access_token)
    
    return user


@router.delete("/{user_id}", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Eliminar usuario (requiere autenticación)"""
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Eliminar usuario usando el use case
    delete_user_use_case = container.delete_user_use_case()
    success = await delete_user_use_case.execute(user_id, access_token)
    
    return DeleteUserResponse(
        success=success,
        message=f"Usuario '{user_id}' eliminado correctamente"
    ) 