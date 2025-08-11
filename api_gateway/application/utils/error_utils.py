"""
Utilidades para manejar errores con códigos específicos
"""
from fastapi import HTTPException, status
from typing import Dict, Any
import ast
from commons.error_codes import ErrorCode


def raise_http_error(
    status_code: int,
    message: str,
    error_code: str,
    **kwargs
) -> None:
    """
    Lanzar HTTPException con código de error específico
    
    Args:
        status_code: Código de estado HTTP
        message: Mensaje de error
        error_code: Código de error específico
        **kwargs: Argumentos adicionales para el error
    """
    detail = {
        "message": message,
        "error_code": error_code,
        **kwargs
    }
    raise HTTPException(status_code=status_code, detail=detail)


def raise_not_found_error(message: str, error_code: str, **kwargs) -> None:
    """Lanzar error 404 con código específico"""
    raise_http_error(
        status_code=status.HTTP_404_NOT_FOUND,
        message=message,
        error_code=error_code,
        **kwargs
    )


def raise_validation_error(message: str, error_code: str, **kwargs) -> None:
    """Lanzar error 400 con código específico"""
    raise_http_error(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=message,
        error_code=error_code,
        **kwargs
    )


def raise_unauthorized_error(message: str, error_code: str, **kwargs) -> None:
    """Lanzar error 401 con código específico"""
    raise_http_error(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message=message,
        error_code=error_code,
        **kwargs
    )


def raise_forbidden_error(message: str, error_code: str, **kwargs) -> None:
    """Lanzar error 403 con código específico"""
    raise_http_error(
        status_code=status.HTTP_403_FORBIDDEN,
        message=message,
        error_code=error_code,
        **kwargs
    )


def raise_conflict_error(message: str, error_code: str, **kwargs) -> None:
    """Lanzar error 409 con código específico"""
    raise_http_error(
        status_code=status.HTTP_409_CONFLICT,
        message=message,
        error_code=error_code,
        **kwargs
    )


def raise_internal_error(message: str, error_code: str, **kwargs) -> None:
    """Lanzar error 500 con código específico"""
    raise_http_error(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=message,
        error_code=error_code,
        **kwargs
    ) 


def parse_auth_service_error(error: Exception) -> tuple[str, str]:
    """
    Parsea errores del auth service que vienen en formato: "500: {'message': '...', 'error_code': '...'}"
    o en formato: "... (ERROR_CODE)"
    
    Args:
        error: La excepción del auth service
        
    Returns:
        tuple: (message, error_code) extraídos del error
    """
    try:
        error_message = str(error)
        
        # Separar la parte después de los ":" para aislar el dict
        if ":" in error_message:
            _, dict_part = error_message.split(":", 1)
            error_dict = ast.literal_eval(dict_part.strip())
            
            message = error_dict.get('message', 'Error desconocido')
            error_code = error_dict.get('error_code', 'INTERNAL_SERVER_ERROR')
            
            return message, error_code
        else:
            # Buscar códigos de error entre paréntesis
            import re
            error_code_match = re.search(r'\(([A-Z_]+)\)', error_message)
            if error_code_match:
                error_code = error_code_match.group(1)
                # Limpiar el mensaje removiendo el código de error
                message = re.sub(r'\s*\([A-Z_]+\).*$', '', error_message).strip()
                return message, error_code
            else:
                # Si no hay ":" ni paréntesis, usar el mensaje completo
                return str(error), 'INTERNAL_SERVER_ERROR'
            
    except Exception:
        # Si falla el parsing, usar el mensaje original
        return str(error), 'INTERNAL_SERVER_ERROR'


def handle_auth_service_error(error: Exception, default_message: str = "Error del servicio de autenticación") -> None:
    """
    Maneja errores del auth service y lanza la excepción apropiada con el código de error correcto.
    
    Args:
        error: La excepción del auth service
        default_message: Mensaje por defecto si no se puede parsear el error
    """
    message, error_code = parse_auth_service_error(error)
    
    # Mapear códigos de error del auth service a nuestros códigos
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
    elif error_code == 'USER_NOT_FOUND':
        raise_not_found_error(
            message="Usuario no encontrado en el sistema de autenticación.",
            error_code=ErrorCode.USER_NOT_FOUND.value
        )
    elif error_code == 'INVALID_TOKEN':
        raise_internal_error(
            message="Token de autenticación inválido.",
            error_code=ErrorCode.UNAUTHORIZED.value
        )
    elif error_code == 'TOKEN_EXPIRED':
        raise_internal_error(
            message="Token de autenticación expirado.",
            error_code=ErrorCode.UNAUTHORIZED.value
        )
    else:
        # Para otros errores, usar el mensaje del auth service
        raise_internal_error(
            message=message or default_message,
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        ) 