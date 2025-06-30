"""
Rutas de administración del API Gateway
"""
from fastapi import APIRouter, Depends, Header
from typing import Optional

router = APIRouter()


@router.get("/users")
async def list_users_admin(authorization: Optional[str] = Header(None)):
    """
    Listar usuarios (admin)
    Redirige al User Service
    """
    return {"message": "Use User Service directly for admin operations"}


@router.post("/users/assign-role")
async def assign_role(authorization: Optional[str] = Header(None)):
    """
    Asignar rol a usuario (admin)
    Redirige al User Service
    """
    return {"message": "Use User Service directly for admin operations"}


@router.delete("/users/{user_id}")
async def delete_user_admin(user_id: str, authorization: Optional[str] = Header(None)):
    """
    Eliminar usuario (admin)
    Redirige al User Service
    """
    return {"message": "Use User Service directly for admin operations"} 