"""
Rutas de autenticación para API Gateway
"""
from fastapi import APIRouter, Depends, status, Header
from typing import Optional
from ...infrastructure.container import Container
from ...domain.auth.dto.requests.auth_requests import (
    ChangePasswordRequest,
    ChangePasswordByUsernameUserRequest,
    ChangePasswordByUsernameCustomerRequest
)
from ...domain.auth.dto.responses.auth_responses import (
    ChangePasswordResponse,
    ChangePasswordByUsernameResponse
)

router = APIRouter()


def get_container() -> Container:
    """Obtener el container de dependencias"""
    return Container()


@router.post("/change-password", response_model=ChangePasswordResponse, status_code=status.HTTP_200_OK)
async def change_password(
    request: ChangePasswordRequest,
    container: Container = Depends(get_container)
):
    """
    Cambiar contraseña de un usuario por su email
    Endpoint para cambiar contraseña de usuario en Firebase
    """
    # Cambiar contraseña usando el use case
    change_password_use_case = container.change_password_use_case()
    result = await change_password_use_case.execute(request)
    
    return result


@router.post("/change-password-by-username-user", response_model=ChangePasswordByUsernameResponse, status_code=status.HTTP_200_OK)
async def change_password_by_username_user(
    request: ChangePasswordByUsernameUserRequest,
    container: Container = Depends(get_container),
    authorization: Optional[str] = Header(None)
):
    """
    Cambiar contraseña de un usuario por su username
    Obtiene el auth_uid del usuario desde el user_service y luego cambia la contraseña en Firebase
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Cambiar contraseña usando el use case
    change_password_use_case = container.change_password_by_username_user_use_case()
    result = await change_password_use_case.execute(request, access_token)
    
    return result


@router.post("/change-password-by-username-customer", response_model=ChangePasswordByUsernameResponse, status_code=status.HTTP_200_OK)
async def change_password_by_username_customer(
    request: ChangePasswordByUsernameCustomerRequest,
    container: Container = Depends(get_container),
    authorization: Optional[str] = Header(None)
):
    """
    Cambiar contraseña de un cliente por su username
    Obtiene el auth_uid del cliente desde el user_service y luego cambia la contraseña en Firebase
    """
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Cambiar contraseña usando el use case
    change_password_use_case = container.change_password_by_username_customer_use_case()
    result = await change_password_use_case.execute(request, access_token)
    
    return result

