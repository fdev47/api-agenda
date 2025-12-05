"""
Manejador centralizado de errores para servicios (auth_service y user_service)
"""
import json
from commons.error_codes import ErrorCode
from commons.error_utils import raise_internal_error, raise_not_found_error, raise_conflict_error


def handle_auth_service_error(error: Exception) -> None:
    """
    Maneja errores del auth service y user service
    
    Args:
        error: Excepción capturada de los servicios
    """
    # Convertir string a dict
    error_str = str(error)
    
    try:
        # Separar la parte después de los ":" para aislar el dict
        _, dict_part = error_str.split(":", 1)
        error_dict = json.loads(dict_part.strip())

        message = error_dict.get('message', 'Mensaje no disponible')
        error_code = error_dict.get('error_code', 'Código no disponible')

        print("Mensaje:", message)
        print("Código de error:", error_code)
        
        # Mapear errores de Auth Service
        if error_code == ErrorCode.PHONE_NUMBER_EXISTS.value:
            raise_conflict_error(
                message="El número de teléfono ya existe en el sistema. Intente con otro número.",
                error_code=ErrorCode.PHONE_NUMBER_EXISTS.value
            )
        elif error_code == ErrorCode.EMAIL_ALREADY_EXISTS.value:
            raise_conflict_error(
                message="El email ya existe en el sistema. Intente con otro email.",
                error_code=ErrorCode.USER_ALREADY_EXISTS.value
            )
        elif error_code == ErrorCode.WEAK_PASSWORD.value:
            raise_internal_error(
                message="La contraseña es demasiado débil.",
                error_code=ErrorCode.VALIDATION_ERROR.value
            )
        elif error_code == ErrorCode.USER_NOT_FOUND.value:
            raise_not_found_error(
                message="Usuario no encontrado en el sistema",
                error_code=ErrorCode.USER_NOT_FOUND.value
            )
        elif error_code == ErrorCode.USER_ALREADY_EXISTS.value:
            raise_conflict_error(
                message="El usuario ya existe en el sistema.",
                error_code=ErrorCode.USER_ALREADY_EXISTS.value
            )
        # Mapear errores de Customer del User Service
        elif error_code == "CUSTOMER_AUTH_UID_ALREADY_EXISTS":
            raise_conflict_error(
                message=message or "Ya existe un proveedor con ese auth_uid",
                error_code="CUSTOMER_AUTH_UID_ALREADY_EXISTS"
            )
        elif error_code == "CUSTOMER_RUC_ALREADY_EXISTS":
            raise_conflict_error(
                message=message or "Ya existe un proveedor con ese RUC",
                error_code="CUSTOMER_RUC_ALREADY_EXISTS"
            )
        elif error_code == "CUSTOMER_EMAIL_ALREADY_EXISTS":
            raise_conflict_error(
                message=message or "Ya existe un proveedor con ese email",
                error_code="CUSTOMER_EMAIL_ALREADY_EXISTS"
            )
        elif error_code == "CUSTOMER_USERNAME_ALREADY_EXISTS":
            raise_conflict_error(
                message=message or "Ya existe un proveedor con ese username",
                error_code="CUSTOMER_USERNAME_ALREADY_EXISTS"
            )
        else:
            # Usar el mensaje del error original
            raise_internal_error(
                message=message,
                error_code=error_code if error_code != 'Código no disponible' else ErrorCode.INTERNAL_SERVER_ERROR.value
            )
    except (ValueError, json.JSONDecodeError) as e:
        # Si no se puede parsear el error, lanzar error genérico
        raise_internal_error(
            message=f"Error en el servicio: {error_str}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )
