"""
Rutas de autenticación para Firebase Auth
"""
import logging
from fastapi import APIRouter, Depends, Header
from typing import Optional
from ...domain.dto.requests import CreateUserRequest, UpdateUserRequest, ChangePasswordRequest
from ...domain.dto.responses import UserInfoResponse
from ...domain.models import UserRegistration, AuthError, AuthErrorCode
from ...domain.exceptions.auth_exceptions import UserNotFoundException
from ...infrastructure.container import container
from commons.error_utils import raise_conflict_error, raise_validation_error, raise_internal_error, raise_not_found_error
from commons.error_codes import ErrorCode

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", response_model=UserInfoResponse)
async def register_user(request: CreateUserRequest):
    """
    Registrar usuario en Firebase
    Endpoint para uso del API Gateway y user_service
    """
    try:
        # Crear usuario en Firebase
        auth_provider = container.auth_provider()
        registration = UserRegistration(
            email=request.email,
            password=request.password,
            display_name=request.display_name,
            phone_number=request.phone_number,
            two_factor_enabled=request.two_factor_enabled,
            send_email_verification=request.send_email_verification
        )
        user = auth_provider.create_user(registration)
        
        # Convertir AuthenticatedUser a UserInfoResponse
        return UserInfoResponse(
            user_id=user.user_id,
            email=user.email,
            display_name=user.display_name,
            phone_number=user.phone_number,
            email_verified=user.email_verified,
            custom_claims=user.custom_claims,
            created_at=user.created_at,
            last_sign_in=user.last_sign_in
        )
    except AuthError as e:
        # Manejar errores específicos de autenticación
        if e.error_code == AuthErrorCode.EMAIL_ALREADY_EXISTS.value:
            raise_conflict_error(
                message="El usuario ya existe en Firebase",
                error_code=ErrorCode.USER_ALREADY_EXISTS.value
            )
        elif e.error_code == AuthErrorCode.PHONE_NUMBER_EXISTS.value:
            raise_conflict_error(
                message="El número de teléfono ya existe en el sistema. Intente con otro número.",
                error_code=ErrorCode.PHONE_NUMBER_EXISTS.value
            )
        elif e.error_code == AuthErrorCode.WEAK_PASSWORD.value:
            raise_validation_error(
                message="La contraseña es demasiado débil",
                error_code=ErrorCode.VALIDATION_ERROR.value
            )
        else:
            raise_validation_error(
                message=str(e),
                error_code=ErrorCode.VALIDATION_ERROR.value
            )
    except Exception as e:
        # Re-lanzar errores inesperados
        raise_internal_error(
            message=f"Error interno del servidor: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.put("/users/{user_id}", response_model=UserInfoResponse)
async def update_user(user_id: str, request: UpdateUserRequest):
    """
    Actualizar usuario en Firebase
    """
    try:
        update_use_case = container.update_user_use_case()
        user = update_use_case.execute(user_id, request)
        return user
    except UserNotFoundException:
        raise_not_found_error(
            message=f"Usuario con ID '{user_id}' no encontrado",
            error_code=ErrorCode.USER_NOT_FOUND.value
        )
    except AuthError as e:
        # Manejar errores específicos de autenticación
        if e.error_code == AuthErrorCode.PHONE_NUMBER_EXISTS.value:
            raise_conflict_error(
                message="El número de teléfono ya existe en el sistema. Intente con otro número.",
                error_code=ErrorCode.PHONE_NUMBER_EXISTS.value
            )
        elif e.error_code == AuthErrorCode.EMAIL_ALREADY_EXISTS.value:
            raise_conflict_error(
                message="El email ya existe en el sistema. Intente con otro email.",
                error_code=ErrorCode.EMAIL_ALREADY_EXISTS.value
            )
        else:
            raise_internal_error(
                message="Error inesperado al actualizar usuario.",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
            )
    except Exception as e:
        raise_internal_error(
            message="Error inesperado al actualizar usuario.",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """
    Eliminar usuario de Firebase
    """
    try:
        delete_use_case = container.delete_user_use_case()
        success = delete_use_case.execute(user_id)
        return {
            "success": success,
            "message": f"Usuario '{user_id}' eliminado correctamente"
        }
    except UserNotFoundException:
        raise_not_found_error(
            message=f"Usuario con ID '{user_id}' no encontrado",
            error_code=ErrorCode.USER_NOT_FOUND.value
        )
    except Exception as e:
        raise_internal_error(
            message=f"Error eliminando usuario: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )


@router.get("/validate-token")
async def validate_token_header(authorization: Optional[str] = Header(None)):
    """
    Validar token de Firebase desde header Authorization
    Endpoint para uso de otros servicios
    """
    if not authorization or not authorization.startswith("Bearer "):
        return {
            "valid": False,
            "message": "Token no proporcionado o formato incorrecto",
            "user": None
        }
    
    token = authorization.replace("Bearer ", "")
    
    try:
        validate_use_case = container.validate_token_use_case()
        user = validate_use_case.execute(token)
        return {
            "valid": True,
            "message": "Token válido",
            "user": {
                "user_id": user.user_id,
                "email": user.email,
                "display_name": user.display_name,
                "email_verified": user.email_verified,
                "custom_claims": user.custom_claims,
                "created_at": user.created_at.isoformat(),
                "last_sign_in": user.last_sign_in.isoformat() if user.last_sign_in else None
            }
        }
    except Exception as e:
        return {
            "valid": False,
            "message": str(e),
            "user": None
        }


@router.get("/validate-token-quick")
async def validate_token_quick(authorization: Optional[str] = Header(None)):
    """
    Validación rápida de token sin obtener datos del usuario.
    Útil para endpoints que solo necesitan verificar si el token es válido.
    Responde mucho más rápido para tokens expirados.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return {
            "valid": False,
            "message": "Token no proporcionado o formato incorrecto"
        }
    
    token = authorization.replace("Bearer ", "")
    
    try:
        # Usar validación rápida directamente
        auth_provider = container.auth_provider()
        is_valid = auth_provider.validate_token_quick(token)
        
        if is_valid:
            return {
                "valid": True,
                "message": "Token válido"
            }
        else:
            return {
                "valid": False,
                "message": "Token inválido o expirado"
            }
    except Exception as e:
        logger.error(f"Error en validación rápida: {e}")
        return {
            "valid": False,
            "message": "Error validando token"
        }


@router.get("/user-info")
async def get_user_info(authorization: Optional[str] = Header(None)):
    """
    Obtener información del usuario autenticado
    """
    if not authorization or not authorization.startswith("Bearer "):
        return {
            "valid": False,
            "message": "Token no proporcionado o formato incorrecto",
            "user": None
        }
    
    token = authorization.replace("Bearer ", "")
    
    try:
        validate_use_case = container.validate_token_use_case()
        user = validate_use_case.execute(token)
        return UserInfoResponse(
            user_id=user.user_id,
            email=user.email,
            display_name=user.display_name,
            phone_number=user.phone_number,
            email_verified=user.email_verified,
            custom_claims=user.custom_claims,
            created_at=user.created_at,
            last_sign_in=user.last_sign_in
        )
    except Exception as e:
        return {
            "valid": False,
            "message": str(e),
            "user": None
        }


@router.post("/change-password")
async def change_password(request: ChangePasswordRequest):
    """
    Cambiar contraseña de un usuario por su email
    Endpoint para cambiar contraseña de usuario en Firebase
    """
    try:
        logger.info(f"🔄 Solicitud de cambio de contraseña para: {request.email}")
        
        change_password_use_case = container.change_password_use_case()
        result = change_password_use_case.execute(request)
        
        return result
        
    except UserNotFoundException as e:
        logger.warning(f"⚠️ Usuario no encontrado: {request.email}")
        raise_not_found_error(
            message=f"Usuario con email '{request.email}' no encontrado",
            error_code=ErrorCode.USER_NOT_FOUND.value
        )
    except AuthError as e:
        # Manejar errores específicos de autenticación
        if e.error_code == AuthErrorCode.WEAK_PASSWORD.value:
            raise_validation_error(
                message="La contraseña es demasiado débil",
                error_code=ErrorCode.VALIDATION_ERROR.value
            )
        else:
            raise_internal_error(
                message=f"Error al cambiar contraseña: {str(e)}",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
            )
    except Exception as e:
        logger.error(f"❌ Error inesperado cambiando contraseña: {str(e)}")
        raise_internal_error(
            message=f"Error interno del servidor: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        ) 