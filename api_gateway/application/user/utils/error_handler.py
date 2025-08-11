"""
Manejador centralizado de errores del auth service para API Gateway
"""
import json
from commons.error_codes import ErrorCode
from commons.error_utils import raise_internal_error


def handle_auth_service_error(error: Exception) -> None:
    """
    Maneja errores del auth service usando tu lógica original
    
    Args:
        error: Excepción capturada del auth service
    """
    # Convertir string a dict
    error_str = str(error)
    
     # Separar la parte después de los ":" para aislar el dict
    _, dict_part = error_str.split(":", 1)
    error_dict = json.loads(dict_part.strip())

    message = error_dict.get('message', 'Mensaje no disponible')
    error_code = error_dict.get('error_code', 'Código no disponible')

    print("Mensaje:", message)
    print("Código de error:", error_code)
    
    # Mapear el código de error a nuestros códigos
    if error_code == 'PHONE_NUMBER_EXISTS':
        raise_internal_error(
            message="El número de teléfono ya existe en el sistema. Intente con otro número.",
            error_code=ErrorCode.PHONE_NUMBER_EXISTS.value
        )
    elif error_code == 'EMAIL_ALREADY_EXISTS':
        raise_internal_error(
            message="El email ya existe en el sistema. Intente con otro email.",
            error_code=ErrorCode.USER_ALREADY_EXISTS.value
        )
    elif error_code == 'WEAK_PASSWORD':
        raise_internal_error(
            message="La contraseña es demasiado débil.",
            error_code=ErrorCode.VALIDATION_ERROR.value
        )
    else:
        # Usar el mensaje del error original
        raise_internal_error(
            message=message,
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )
