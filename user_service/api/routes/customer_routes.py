"""
Rutas para Customer
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.dto.requests.customer_requests import CreateCustomerRequest, UpdateCustomerRequest
from ...domain.dto.responses.customer_responses import (
    CustomerResponse,
    CustomerListResponse,
    CustomerUpdatedResponse,
    CustomerDeletedResponse
)
from ...application.use_cases.create_customer_use_case import CreateCustomerUseCase
from ...application.use_cases.get_customer_use_case import GetCustomerUseCase
from ...application.use_cases.list_customers_use_case import ListCustomersUseCase
from ...application.use_cases.update_customer_use_case import UpdateCustomerUseCase
from ...application.use_cases.delete_customer_use_case import DeleteCustomerUseCase
from ...infrastructure.container import container
from ...infrastructure.connection import get_db_session
from ...domain.exceptions.user_exceptions import (
    UserException, 
    UserNotFoundException,
    CustomerAuthUidAlreadyExistsException,
    CustomerRucAlreadyExistsException,
    CustomerEmailAlreadyExistsException,
    CustomerUsernameAlreadyExistsException
)
from ..middleware import auth_middleware
from commons.error_utils import raise_not_found_error, raise_internal_error, raise_conflict_error
from commons.error_codes import ErrorCode

router = APIRouter(tags=["Customers"])

@router.get("/me", response_model=CustomerResponse)
async def get_current_customer_info(
    current_user=Depends(auth_middleware["require_auth_full"]),
    db: AsyncSession = Depends(get_db_session)
):
    """Obtener información del customer actual"""
    try:
        auth_uid = current_user["user_id"]
        
        container.db_session.override(db)
        get_current_use_case = container.get_current_customer_use_case()
        result = await get_current_use_case.execute(auth_uid)
        return result
        
    except UserNotFoundException as e:
        raise_not_found_error(
            message="Customer no encontrado en el sistema",
            error_code=ErrorCode.USER_NOT_FOUND.value
        )
    except UserException as e:
        raise_internal_error(
            message=f"Error obteniendo customer: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )
    except Exception as e:
        raise_internal_error(
            message=f"Error inesperado: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )

@router.post("/", response_model=CustomerResponse)
async def create_customer(
    request: CreateCustomerRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """Crear un nuevo customer"""
    try:
        container.db_session.override(db)
        create_use_case = container.create_customer_use_case()
        result = await create_use_case.execute(request)
        return result
    except CustomerAuthUidAlreadyExistsException as e:
        raise_conflict_error(
            message=f"Ya existe un proveedor con el auth_uid '{request.auth_uid}'",
            error_code="CUSTOMER_AUTH_UID_ALREADY_EXISTS"
        )
    except CustomerRucAlreadyExistsException as e:
        raise_conflict_error(
            message=f"Ya existe un proveedor con el RUC '{request.ruc}'",
            error_code="CUSTOMER_RUC_ALREADY_EXISTS"
        )
    except CustomerEmailAlreadyExistsException as e:
        raise_conflict_error(
            message=f"Ya existe un proveedor con el email '{request.email}'",
            error_code="CUSTOMER_EMAIL_ALREADY_EXISTS"
        )
    except CustomerUsernameAlreadyExistsException as e:
        raise_conflict_error(
            message=f"Ya existe un proveedor con el username '{request.username}'",
            error_code="CUSTOMER_USERNAME_ALREADY_EXISTS"
        )
    except UserException as e:
        raise_internal_error(
            message=f"Error al crear proveedor: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )
    except Exception as e:
        raise_internal_error(
            message=f"Error inesperado: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )

@router.get("/", response_model=CustomerListResponse)
async def get_customers(
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de elementos"),
    username: Optional[str] = Query(None, description="Filtrar por username (búsqueda parcial)"),
    company_name: Optional[str] = Query(None, description="Filtrar por nombre de empresa (búsqueda parcial)"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    ruc: Optional[str] = Query(None, description="Filtrar por RUC"),
    address_id: Optional[UUID] = Query(None, description="Filtrar por ID de dirección"),
    db: AsyncSession = Depends(get_db_session)
):
    """Obtener todos los customers con filtros opcionales"""
    try:
        container.db_session.override(db)
        list_use_case = container.list_customers_use_case()
        result = await list_use_case.execute(
            skip=skip, 
            limit=limit,
            username=username,
            company_name=company_name,
            is_active=is_active,
            ruc=ruc,
            address_id=address_id
        )
        return result
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """Obtener un customer por ID"""
    try:
        container.db_session.override(db)
        get_use_case = container.get_customer_use_case()
        result = await get_use_case.execute(customer_id)
        return result
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/by-username/{username}", response_model=CustomerResponse)
async def get_customer_by_username(
    username: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Obtener un customer por username"""
    try:
        # Inyectar la sesión de base de datos en el contenedor
        container.db_session.override(db)
        get_use_case = container.get_customer_by_username_use_case()
        result = await get_use_case.execute(username)
        return result
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.put("/{customer_id}", response_model=CustomerUpdatedResponse)
async def update_customer(
    customer_id: UUID, 
    request: UpdateCustomerRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """Actualizar un customer"""
    try:
        container.db_session.override(db)
        update_use_case = container.update_customer_use_case()
        result = await update_use_case.execute(customer_id, request)
        return result
    except UserNotFoundException as e:
        raise_not_found_error(
            message=f"Customer con ID '{customer_id}' no encontrado",
            error_code=ErrorCode.USER_NOT_FOUND.value
        )
    except CustomerAuthUidAlreadyExistsException as e:
        raise_conflict_error(
            message=f"Ya existe un proveedor con el auth_uid proporcionado",
            error_code="CUSTOMER_AUTH_UID_ALREADY_EXISTS"
        )
    except CustomerRucAlreadyExistsException as e:
        raise_conflict_error(
            message=f"Ya existe un proveedor con el RUC proporcionado",
            error_code="CUSTOMER_RUC_ALREADY_EXISTS"
        )
    except CustomerEmailAlreadyExistsException as e:
        raise_conflict_error(
            message=f"Ya existe un proveedor con el email proporcionado",
            error_code="CUSTOMER_EMAIL_ALREADY_EXISTS"
        )
    except CustomerUsernameAlreadyExistsException as e:
        raise_conflict_error(
            message=f"Ya existe un proveedor con el username proporcionado",
            error_code="CUSTOMER_USERNAME_ALREADY_EXISTS"
        )
    except UserException as e:
        raise_internal_error(
            message=f"Error al actualizar proveedor: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )
    except Exception as e:
        raise_internal_error(
            message=f"Error inesperado: {str(e)}",
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
        )

@router.delete("/{customer_id}", response_model=CustomerDeletedResponse)
async def delete_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """Eliminar un customer"""
    try:
        container.db_session.override(db)
        delete_use_case = container.delete_customer_use_case()
        result = await delete_use_case.execute(customer_id)
        return result
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}") 