"""
Rutas de perfiles en el API Gateway
"""
from fastapi import APIRouter, Depends, Query, Header
from typing import List, Optional
from ...domain.profile.dto.responses.profile_responses import ProfileListResponse
from ...application.profile.use_cases.list_profiles_use_case import ListProfilesUseCase
from ..middleware import auth_middleware

router = APIRouter()

@router.get("/", response_model=ProfileListResponse)
async def list_profiles(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Listar perfiles disponibles
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    use_case = ListProfilesUseCase()
    profiles = await use_case.execute(skip=skip, limit=limit, access_token=access_token)
    
    return ProfileListResponse(
        profiles=profiles,
        total=len(profiles),
        skip=skip,
        limit=limit
    ) 