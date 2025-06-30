"""
Middleware para manejo de errores en el servicio de ubicaciones
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Union
import traceback

from ..domain.exceptions.location_exceptions import LocationDomainException
from ..domain.exceptions.local_exceptions import (
    LocalNotFoundException, LocalAlreadyExistsException, LocalValidationException
)
from ..domain.exceptions.branch_exceptions import (
    BranchNotFoundException, BranchAlreadyExistsException, BranchValidationException
)
from ..domain.dto.responses.error_responses import (
    ErrorResponse, ValidationErrorResponse, LocationErrorResponse,
    NotFoundErrorResponse, ConflictErrorResponse
)


async def error_handler_middleware(request: Request, call_next):
    """Middleware para manejo centralizado de errores"""
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        return await handle_exception(request, exc)


async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
    """Manejar excepciones y convertirlas a responses de error consistentes"""
    timestamp = datetime.utcnow().isoformat()
    
    # Mapear excepciones específicas del dominio
    if isinstance(exc, LocalNotFoundException):
        return JSONResponse(
            status_code=404,
            content=NotFoundErrorResponse(
                error="not_found",
                message=str(exc),
                entity_type="local",
                entity_id=getattr(exc, 'entity_id', None),
                timestamp=timestamp
            ).dict()
        )
    
    elif isinstance(exc, LocalAlreadyExistsException):
        return JSONResponse(
            status_code=409,
            content=ConflictErrorResponse(
                error="conflict",
                message=str(exc),
                entity_type="local",
                field_name="code",
                field_value=getattr(exc, 'code', None),
                timestamp=timestamp
            ).dict()
        )
    
    elif isinstance(exc, LocalValidationException):
        return JSONResponse(
            status_code=400,
            content=ValidationErrorResponse(
                error="validation_error",
                message=str(exc),
                field_errors=getattr(exc, 'field_errors', {}),
                timestamp=timestamp
            ).dict()
        )
    
    elif isinstance(exc, BranchNotFoundException):
        return JSONResponse(
            status_code=404,
            content=NotFoundErrorResponse(
                error="not_found",
                message=str(exc),
                entity_type="branch",
                entity_id=getattr(exc, 'entity_id', None),
                timestamp=timestamp
            ).dict()
        )
    
    elif isinstance(exc, BranchAlreadyExistsException):
        return JSONResponse(
            status_code=409,
            content=ConflictErrorResponse(
                error="conflict",
                message=str(exc),
                entity_type="branch",
                field_name="code",
                field_value=getattr(exc, 'code', None),
                timestamp=timestamp
            ).dict()
        )
    
    elif isinstance(exc, BranchValidationException):
        return JSONResponse(
            status_code=400,
            content=ValidationErrorResponse(
                error="validation_error",
                message=str(exc),
                field_errors=getattr(exc, 'field_errors', {}),
                timestamp=timestamp
            ).dict()
        )
    
    elif isinstance(exc, LocationDomainException):
        return JSONResponse(
            status_code=400,
            content=LocationErrorResponse(
                error="location_error",
                message=str(exc),
                error_code=getattr(exc, 'error_code', None),
                entity_type=getattr(exc, 'entity_type', None),
                entity_id=getattr(exc, 'entity_id', None),
                timestamp=timestamp
            ).dict()
        )
    
    elif isinstance(exc, HTTPException):
        # Manejar HTTPExceptions de FastAPI
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="http_error",
                message=exc.detail,
                error_code=f"HTTP_{exc.status_code}",
                timestamp=timestamp
            ).dict()
        )
    
    else:
        # Error interno del servidor
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="internal_server_error",
                message="Error interno del servidor",
                error_code="INTERNAL_ERROR",
                details={
                    "exception_type": type(exc).__name__,
                    "traceback": traceback.format_exc() if request.app.debug else None
                },
                timestamp=timestamp
            ).dict()
        )


def create_error_response(
    error_type: str,
    message: str,
    status_code: int = 400,
    error_code: str = None,
    entity_type: str = None,
    entity_id: int = None,
    field_errors: dict = None,
    field_name: str = None,
    field_value: str = None,
    details: dict = None
) -> JSONResponse:
    """Función helper para crear responses de error consistentes"""
    timestamp = datetime.utcnow().isoformat()
    
    if error_type == "not_found":
        content = NotFoundErrorResponse(
            error="not_found",
            message=message,
            entity_type=entity_type,
            entity_id=entity_id,
            timestamp=timestamp
        ).dict()
    
    elif error_type == "conflict":
        content = ConflictErrorResponse(
            error="conflict",
            message=message,
            entity_type=entity_type,
            field_name=field_name,
            field_value=field_value,
            timestamp=timestamp
        ).dict()
    
    elif error_type == "validation_error":
        content = ValidationErrorResponse(
            error="validation_error",
            message=message,
            field_errors=field_errors or {},
            timestamp=timestamp
        ).dict()
    
    elif error_type == "location_error":
        content = LocationErrorResponse(
            error="location_error",
            message=message,
            error_code=error_code,
            entity_type=entity_type,
            entity_id=entity_id,
            timestamp=timestamp
        ).dict()
    
    else:
        content = ErrorResponse(
            error=error_type,
            message=message,
            error_code=error_code,
            details=details,
            timestamp=timestamp
        ).dict()
    
    return JSONResponse(status_code=status_code, content=content) 