"""
Utilidades para manejar errores con códigos específicos
"""
from fastapi import HTTPException, status
from typing import Dict, Any


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