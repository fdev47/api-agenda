"""
Rutas de usuarios del API Gateway
"""
from fastapi import APIRouter, Depends, Header
from typing import Optional

router = APIRouter()


@router.get("/")
async def list_users(authorization: Optional[str] = Header(None)):
    """
    Listar usuarios
    Redirige al User Service
    """
    return {"message": "Use User Service directly for user operations"}


@router.post("/")
async def create_user(authorization: Optional[str] = Header(None)):
    """
    Crear usuario
    Redirige al User Service
    """
    return {"message": "Use User Service directly for user operations"}


@router.get("/{user_id}")
async def get_user(user_id: str, authorization: Optional[str] = Header(None)):
    """
    Obtener usuario por ID
    Redirige al User Service
    """
    return {"message": "Use User Service directly for user operations"}


@router.put("/{user_id}")
async def update_user(user_id: str, authorization: Optional[str] = Header(None)):
    """
    Actualizar usuario
    Redirige al User Service
    """
    return {"message": "Use User Service directly for user operations"}


@router.delete("/{user_id}")
async def delete_user(user_id: str, authorization: Optional[str] = Header(None)):
    """
    Eliminar usuario
    Redirige al User Service
    """
    return {"message": "Use User Service directly for user operations"} 