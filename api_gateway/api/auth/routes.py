"""
Rutas de autenticación para API Gateway
"""
from fastapi import APIRouter, Depends, status
from ...infrastructure.container import Container
from ...domain.auth.dto.requests.auth_requests import ChangePasswordRequest
from ...domain.auth.dto.responses.auth_responses import ChangePasswordResponse

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

