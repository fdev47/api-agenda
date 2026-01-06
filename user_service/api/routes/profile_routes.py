"""
Rutas de perfiles
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.dto.requests import CreateProfileRequest, UpdateProfileRequest
from ...domain.dto.responses import ProfileResponse, ProfileListResponse, SuccessResponse
from ...infrastructure.container import container
from ...infrastructure.connection import get_db_session
from ..middleware import auth_middleware
from commons.error_utils import raise_not_found_error, raise_internal_error
from commons.error_codes import ErrorCode

router = APIRouter()


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    request: CreateProfileRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Crear un nuevo perfil"""
    try:
        container.db_session.override(db)
        create_use_case = container.create_profile_use_case()
        profile = await create_use_case.execute(request)
        return profile
    except Exception as e:
        raise_internal_error(
            message=f"Error creando perfil: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile_by_id(
    profile_id: UUID,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Obtener perfil por ID"""
    try:
        container.db_session.override(db)
        get_use_case = container.get_profile_by_id_use_case()
        profile = await get_use_case.execute(profile_id)
        return profile
    except Exception as e:
        if "ProfileNotFoundException" in str(e):
            raise_not_found_error(
                message="Perfil no encontrado",
                error_code=ErrorCode.PROFILE_NOT_FOUND.value
            )
        raise_internal_error(
            message=f"Error obteniendo perfil: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.get("/", response_model=ProfileListResponse)
async def list_profiles(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Listar perfiles"""
    try:
        container.db_session.override(db)
        list_use_case = container.list_profiles_use_case()
        profiles = await list_use_case.execute(skip=skip, limit=limit)
        return ProfileListResponse(
            profiles=profiles,
            total=len(profiles),
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise_internal_error(
            message=f"Error listando perfiles: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.put("/{profile_id}", response_model=ProfileResponse)
async def update_profile(
    profile_id: UUID,
    request: UpdateProfileRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Actualizar perfil"""
    try:
        container.db_session.override(db)
        update_use_case = container.update_profile_use_case()
        profile = await update_use_case.execute(profile_id, request)
        return profile
    except Exception as e:
        if "ProfileNotFoundException" in str(e):
            raise_not_found_error(
                message="Perfil no encontrado",
                error_code=ErrorCode.PROFILE_NOT_FOUND.value
            )
        raise_internal_error(
            message=f"Error actualizando perfil: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.delete("/{profile_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def delete_profile(
    profile_id: UUID,
    current_user=Depends(auth_middleware["require_auth"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Eliminar perfil"""
    try:
        container.db_session.override(db)
        delete_use_case = container.delete_profile_use_case()
        success = await delete_use_case.execute(profile_id)
        return SuccessResponse(
            success=True,
            message=f"Perfil {profile_id} eliminado exitosamente"
        )
    except Exception as e:
        if "ProfileNotFoundException" in str(e):
            raise_not_found_error(
                message="Perfil no encontrado",
                error_code=ErrorCode.PROFILE_NOT_FOUND.value
            )
        raise_internal_error(
            message=f"Error eliminando perfil: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        ) 