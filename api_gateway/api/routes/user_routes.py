"""
Rutas de usuarios para API Gateway
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from typing import Optional
from ...infrastructure.container import Container
from ..middleware import auth_middleware
from ...domain.dto.responses.user import UserResponse, UserListResponse

router = APIRouter()


def get_container() -> Container:
    """Obtener el container de dependencias"""
    return Container()


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